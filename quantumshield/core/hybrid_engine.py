"""Hybrid AES-256-GCM + ML-KEM (Kyber) file pipeline."""

from __future__ import annotations

from .aes_module import AES_KEY_SIZE_BYTES, decrypt_bytes, encrypt_bytes
from .kyber_module import decapsulate, encapsulate
from .package_format import build_package, parse_package


def _derive_aes_key(shared_secret: bytes) -> bytes:
    if len(shared_secret) < AES_KEY_SIZE_BYTES:
        raise ValueError("shared secret too short for AES-256")
    return shared_secret[:AES_KEY_SIZE_BYTES]


def encrypt_file(input_path: str, output_path: str, public_key: bytes) -> None:
    """Encrypt a file and write a packaged hybrid ciphertext.

    Steps:
        1) Encapsulate a shared secret using Kyber
        2) Derive AES session key from the shared secret
        3) Encrypt file using AES-GCM
        4) Build encrypted package
        5) Save package to output file
    """

    with open(input_path, "rb") as file_in:
        plaintext = file_in.read()

    kem_ciphertext, shared_secret = encapsulate(public_key)
    aes_key = _derive_aes_key(shared_secret)

    ciphertext, nonce, tag = encrypt_bytes(plaintext, aes_key)
    package = build_package(kem_ciphertext, nonce, tag, ciphertext)

    with open(output_path, "wb") as file_out:
        file_out.write(package)


def decrypt_file(input_path: str, output_path: str, secret_key: bytes) -> None:
    """Decrypt a packaged hybrid ciphertext file.

    Steps:
        1) Read encrypted package
        2) Parse package
        3) Decapsulate AES key using Kyber
        4) Decrypt AES ciphertext
        5) Write original file
    """

    with open(input_path, "rb") as file_in:
        data = file_in.read()

    kem_ciphertext, nonce, tag, ciphertext = parse_package(data)
    shared_secret = decapsulate(kem_ciphertext, secret_key)
    aes_key = _derive_aes_key(shared_secret)

    plaintext = decrypt_bytes(ciphertext, aes_key, nonce, tag)

    with open(output_path, "wb") as file_out:
        file_out.write(plaintext)