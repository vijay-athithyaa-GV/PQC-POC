"""Crypto-agility interfaces and default implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from . import aes_module
from . import kyber_module


class SymmetricCipher(ABC):
    """Abstract symmetric cipher interface."""

    @abstractmethod
    def encrypt(self, data: bytes, key: bytes) -> Tuple[bytes, bytes, bytes]:
        """Encrypt data and return (ciphertext, nonce, tag)."""

    @abstractmethod
    def decrypt(self, ciphertext: bytes, key: bytes, nonce: bytes, tag: bytes) -> bytes:
        """Decrypt data and return plaintext."""


class KeyEncapsulation(ABC):
    """Abstract KEM interface."""

    @abstractmethod
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """Return (public_key, secret_key)."""

    @abstractmethod
    def encapsulate(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """Return (ciphertext, shared_secret)."""

    @abstractmethod
    def decapsulate(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        """Return shared_secret from ciphertext and secret_key."""


class AESGCMCipher(SymmetricCipher):
    """AES-256-GCM wrapper for the crypto-agility layer."""

    def encrypt(self, data: bytes, key: bytes) -> Tuple[bytes, bytes, bytes]:
        return aes_module.encrypt_bytes(data, key)

    def decrypt(self, ciphertext: bytes, key: bytes, nonce: bytes, tag: bytes) -> bytes:
        return aes_module.decrypt_bytes(ciphertext, key, nonce, tag)


class KyberKEM(KeyEncapsulation):
    """ML-KEM (Kyber) wrapper for the crypto-agility layer."""

    def __init__(self, algorithm: str = kyber_module.DEFAULT_KEM_ALGORITHM) -> None:
        self._algorithm = algorithm

    def generate_keypair(self) -> Tuple[bytes, bytes]:
        return kyber_module.generate_keypair(self._algorithm)

    def encapsulate(self, public_key: bytes) -> Tuple[bytes, bytes]:
        return kyber_module.encapsulate(public_key, self._algorithm)

    def decapsulate(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        return kyber_module.decapsulate(ciphertext, secret_key, self._algorithm)
