"""Hybrid AES-256-GCM + ML-KEM (Kyber) file pipeline."""

from __future__ import annotations

from .aes_module import AES_KEY_SIZE_BYTES
from .crypto_agility import AESGCMCipher, KyberKEM, KeyEncapsulation, SymmetricCipher
from .package_format import build_package, parse_package


def _derive_aes_key(shared_secret: bytes) -> bytes:
    if len(shared_secret) < AES_KEY_SIZE_BYTES:
        raise ValueError("shared secret too short for AES-256")
    return shared_secret[:AES_KEY_SIZE_BYTES]


def _validate_paths(input_path: str, output_path: str) -> None:
    if not isinstance(input_path, str) or not input_path:
        raise ValueError("input_path must be a non-empty string")
    if not isinstance(output_path, str) or not output_path:
        raise ValueError("output_path must be a non-empty string")
    if input_path == output_path:
        raise ValueError("input_path and output_path must be different")


def _read_file(path: str) -> bytes:
    try:
        with open(path, "rb") as file_in:
            return file_in.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"input file not found: {path}") from exc
    except OSError as exc:
        raise OSError(f"failed to read input file: {path}") from exc


def _write_file(path: str, data: bytes) -> None:
    try:
        with open(path, "wb") as file_out:
            file_out.write(data)
    except OSError as exc:
        raise OSError(f"failed to write output file: {path}") from exc


def encrypt_file(
    input_path: str,
    output_path: str,
    public_key: bytes,
    *,
    kem: KeyEncapsulation | None = None,
    cipher: SymmetricCipher | None = None,
) -> None:
    """Encrypt a file and write a packaged hybrid ciphertext.

    Steps:
        1) Encapsulate a shared secret using Kyber
        2) Derive AES session key from the shared secret
        3) Encrypt file using AES-GCM
        4) Build encrypted package
        5) Save package to output file
    """

    _validate_paths(input_path, output_path)

    plaintext = _read_file(input_path)

    kem_impl = kem or KyberKEM()
    cipher_impl = cipher or AESGCMCipher()

    kem_ciphertext, shared_secret = kem_impl.encapsulate(public_key)
    aes_key = _derive_aes_key(shared_secret)

    ciphertext, nonce, tag = cipher_impl.encrypt(plaintext, aes_key)
    package = build_package(kem_ciphertext, nonce, tag, ciphertext)

    _write_file(output_path, package)


def decrypt_file(
    input_path: str,
    output_path: str,
    secret_key: bytes,
    *,
    kem: KeyEncapsulation | None = None,
    cipher: SymmetricCipher | None = None,
) -> None:
    """Decrypt a packaged hybrid ciphertext file.

    Steps:
        1) Read encrypted package
        2) Parse package
        3) Decapsulate AES key using Kyber
        4) Decrypt AES ciphertext
        5) Write original file
    """

    _validate_paths(input_path, output_path)

    data = _read_file(input_path)

    kem_impl = kem or KyberKEM()
    cipher_impl = cipher or AESGCMCipher()

    try:
        kem_ciphertext, nonce, tag, ciphertext = parse_package(data)
        shared_secret = kem_impl.decapsulate(kem_ciphertext, secret_key)
        aes_key = _derive_aes_key(shared_secret)
        plaintext = cipher_impl.decrypt(ciphertext, aes_key, nonce, tag)
    except ValueError as exc:
        raise ValueError("failed to decrypt package: invalid or corrupted data") from exc

    _write_file(output_path, plaintext)


def encrypt_pipeline(input_path: str, output_path: str, public_key: bytes) -> None:
    """Compatibility wrapper for the hybrid encryption pipeline."""

    encrypt_file(input_path, output_path, public_key)


def decrypt_pipeline(input_path: str, output_path: str, secret_key: bytes) -> None:
    """Compatibility wrapper for the hybrid decryption pipeline."""

    decrypt_file(input_path, output_path, secret_key)