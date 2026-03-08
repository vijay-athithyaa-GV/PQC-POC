"""
Crypto-Agility Abstraction Layer
Allows cryptographic algorithms to be replaced without changing system logic.
"""

from abc import ABC, abstractmethod


class SymmetricCipher(ABC):

    @abstractmethod
    def encrypt(self, plaintext: bytes, key: bytes):
        pass

    @abstractmethod
    def decrypt(self, ciphertext: bytes, key: bytes, nonce: bytes, tag: bytes):
        pass


class KeyEncapsulationMechanism(ABC):

    @abstractmethod
    def generate_keypair(self):
        pass

    @abstractmethod
    def encapsulate(self, public_key: bytes):
        pass

    @abstractmethod
    def decapsulate(self, ciphertext: bytes, secret_key: bytes):
        pass
