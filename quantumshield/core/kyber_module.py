"""ML-KEM (Kyber) key encapsulation using liboqs-python.

This module provides standalone post-quantum KEM operations and does not
integrate with AES yet (Day 3 scope only).
"""

from __future__ import annotations

from typing import Tuple

import oqs

DEFAULT_KEM_ALGORITHM = "ML-KEM-768"


def _validate_bytes(value: bytes, name: str) -> None:
    if not isinstance(value, (bytes, bytearray)):
        raise TypeError(f"{name} must be bytes")


def generate_keypair(algorithm: str = DEFAULT_KEM_ALGORITHM) -> Tuple[bytes, bytes]:
    """Generate an ML-KEM keypair.

    Args:
        algorithm: liboqs algorithm name, default is ML-KEM-768.

    Returns:
        A tuple of (public_key, secret_key).
    """

    with oqs.KeyEncapsulation(algorithm) as kem:
        public_key = kem.generate_keypair()
        secret_key = kem.export_secret_key()
    return public_key, secret_key


def encapsulate(public_key: bytes, algorithm: str = DEFAULT_KEM_ALGORITHM) -> Tuple[bytes, bytes]:
    """Encapsulate a shared secret to a public key.

    Cryptography overview:
        - Generate a random shared secret.
        - Encrypt it to the recipient's public key to produce a KEM ciphertext.

    Args:
        public_key: Recipient's ML-KEM public key.
        algorithm: liboqs algorithm name, default is ML-KEM-768.

    Returns:
        A tuple of (ciphertext, shared_secret).
    """

    _validate_bytes(public_key, "public_key")

    with oqs.KeyEncapsulation(algorithm) as kem:
        kem.import_public_key(bytes(public_key))
        ciphertext, shared_secret = kem.encap_secret()
    return ciphertext, shared_secret


def decapsulate(ciphertext: bytes, secret_key: bytes, algorithm: str = DEFAULT_KEM_ALGORITHM) -> bytes:
    """Decapsulate a shared secret from a KEM ciphertext.

    Cryptography overview:
        - Decrypt the ciphertext using the secret key.
        - Recover the same shared secret created during encapsulation.

    Args:
        ciphertext: KEM ciphertext produced by encapsulate().
        secret_key: ML-KEM secret key.
        algorithm: liboqs algorithm name, default is ML-KEM-768.

    Returns:
        The recovered shared secret.
    """

    _validate_bytes(ciphertext, "ciphertext")
    _validate_bytes(secret_key, "secret_key")

    with oqs.KeyEncapsulation(algorithm) as kem:
        kem.import_secret_key(bytes(secret_key))
        shared_secret = kem.decap_secret(bytes(ciphertext))
    return shared_secret
