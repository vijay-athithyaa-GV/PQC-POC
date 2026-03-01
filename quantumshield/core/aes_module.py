"""AES-256-GCM utilities for byte and file encryption.

Day 1: byte-level encrypt/decrypt helpers.
Day 2: file-level encrypt/decrypt with a simple container format.
"""

from __future__ import annotations

from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

AES_KEY_SIZE_BYTES = 32
GCM_NONCE_SIZE_BYTES = 12
GCM_TAG_SIZE_BYTES = 16


def generate_aes_key() -> bytes:
    """Generate a 256-bit AES key using a CSPRNG.

    Returns:
        A 32-byte key suitable for AES-256.
    """

    return get_random_bytes(AES_KEY_SIZE_BYTES)


def _validate_key(key: bytes) -> None:
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes")
    if len(key) != AES_KEY_SIZE_BYTES:
        raise ValueError("key must be 32 bytes for AES-256")


def encrypt_bytes(data: bytes, key: bytes) -> Tuple[bytes, bytes, bytes]:
    """Encrypt data using AES-256-GCM.

    Args:
        data: Plaintext bytes to encrypt.
        key: 32-byte AES key.

    Returns:
        A tuple of (ciphertext, nonce, tag).
    """

    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    _validate_key(key)

    nonce = get_random_bytes(GCM_NONCE_SIZE_BYTES)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return ciphertext, nonce, tag


def decrypt_bytes(ciphertext: bytes, key: bytes, nonce: bytes, tag: bytes) -> bytes:
    """Decrypt data using AES-256-GCM.

    Args:
        ciphertext: Encrypted bytes.
        key: 32-byte AES key.
        nonce: GCM nonce used during encryption.
        tag: Authentication tag from encryption.

    Returns:
        The decrypted plaintext bytes.

    Raises:
        ValueError: If authentication fails or inputs are invalid.
    """

    if not isinstance(ciphertext, (bytes, bytearray)):
        raise TypeError("ciphertext must be bytes")
    if not isinstance(nonce, (bytes, bytearray)):
        raise TypeError("nonce must be bytes")
    if not isinstance(tag, (bytes, bytearray)):
        raise TypeError("tag must be bytes")
    _validate_key(key)

    if len(nonce) != GCM_NONCE_SIZE_BYTES:
        raise ValueError("nonce must be 12 bytes for GCM")
    if len(tag) != GCM_TAG_SIZE_BYTES:
        raise ValueError("tag must be 16 bytes for GCM")

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        return cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError as exc:
        raise ValueError("authentication failed or data corrupted") from exc


def encrypt_file(input_path: str, output_path: str) -> bytes:
    """Encrypt a file with AES-256-GCM.

    File format:
        [12 bytes nonce][16 bytes tag][ciphertext]

    Args:
        input_path: Path to plaintext file.
        output_path: Path to write encrypted file.

    Returns:
        The generated 32-byte AES key.
    """

    with open(input_path, "rb") as file_in:
        plaintext = file_in.read()

    key = generate_aes_key()
    ciphertext, nonce, tag = encrypt_bytes(plaintext, key)

    with open(output_path, "wb") as file_out:
        file_out.write(nonce + tag + ciphertext)

    return key


def decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """Decrypt a file encrypted by encrypt_file().

    Args:
        input_path: Path to encrypted file.
        output_path: Path to write decrypted file.
        key: 32-byte AES key.
    """

    _validate_key(key)

    with open(input_path, "rb") as file_in:
        blob = file_in.read()

    header_size = GCM_NONCE_SIZE_BYTES + GCM_TAG_SIZE_BYTES
    if len(blob) < header_size:
        raise ValueError("encrypted file is too short")

    nonce = blob[:GCM_NONCE_SIZE_BYTES]
    tag = blob[GCM_NONCE_SIZE_BYTES:header_size]
    ciphertext = blob[header_size:]

    plaintext = decrypt_bytes(ciphertext, key, nonce, tag)

    with open(output_path, "wb") as file_out:
        file_out.write(plaintext)
