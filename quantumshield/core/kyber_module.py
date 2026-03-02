"""
ML-KEM (Kyber) key encapsulation using liboqs-python.
Compatible with older liboqs-python builds.
"""

from __future__ import annotations
from typing import Tuple
import oqs

DEFAULT_KEM_ALGORITHM = "ML-KEM-768"


def _validate_bytes(value: bytes, name: str) -> None:
    if not isinstance(value, (bytes, bytearray)):
        raise TypeError(f"{name} must be bytes")


def generate_keypair(
    algorithm: str = DEFAULT_KEM_ALGORITHM,
) -> Tuple[bytes, bytes]:

    with oqs.KeyEncapsulation(algorithm) as kem:
        public_key = kem.generate_keypair()
        secret_key = kem.export_secret_key()

    return public_key, secret_key


def encapsulate(
    public_key: bytes,
    algorithm: str = DEFAULT_KEM_ALGORITHM,
) -> Tuple[bytes, bytes]:

    _validate_bytes(public_key, "public_key")

    with oqs.KeyEncapsulation(algorithm) as kem:
        ciphertext, shared_secret = kem.encap_secret(public_key)

    return ciphertext, shared_secret


def decapsulate(
    ciphertext: bytes,
    secret_key: bytes,
    algorithm: str = DEFAULT_KEM_ALGORITHM,
) -> bytes:

    _validate_bytes(ciphertext, "ciphertext")
    _validate_bytes(secret_key, "secret_key")

    # 🔥 Pass secret_key directly to constructor
    with oqs.KeyEncapsulation(algorithm, secret_key=secret_key) as kem:
        shared_secret = kem.decap_secret(ciphertext)

    return shared_secret