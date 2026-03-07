"""
Hybrid AES-256-GCM + ML-KEM encryption engine.

Fully stable version with:
- Proper AES key wrapping
- liboqs decapsulation fix
- Clean metadata packaging
"""

from __future__ import annotations

import json
import base64

from .aes_module import encrypt_file, decrypt_file
from .kyber_module import generate_keypair, encapsulate, decapsulate


class HybridEngine:
    """
    Hybrid post-quantum encryption engine.
    Combines:
        - AES-256-GCM for file encryption
        - ML-KEM (Kyber) for key encapsulation
    """

    def __init__(self, kem_algorithm: str = "ML-KEM-768"):
        self.kem_algorithm = kem_algorithm

    # -------------------------
    # Utility: base64 encoding
    # -------------------------

    @staticmethod
    def _b64_encode(data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def _b64_decode(data: str) -> bytes:
        return base64.b64decode(data.encode("utf-8"))

    # -------------------------
    # Encrypt
    # -------------------------

    def encrypt(self, input_file: str, encrypted_file: str, metadata_file: str) -> None:
        """
        Encrypt a file using AES-256-GCM.
        Wrap the AES key using ML-KEM shared secret.
        """

        print("🔐 Starting AES file encryption...")
        aes_key = encrypt_file(input_file, encrypted_file)

        print("🔑 Generating ML-KEM keypair...")
        public_key, secret_key = generate_keypair(self.kem_algorithm)

        print("📦 Encapsulating shared secret...")
        kem_ciphertext, shared_secret = encapsulate(
            public_key,
            self.kem_algorithm,
        )

        # Derive wrapping key from shared secret
        wrapping_key = shared_secret[:32]  # AES-256

        # Wrap AES key using AES-GCM
        from Crypto.Cipher import AES
        from Crypto.Random import get_random_bytes

        nonce = get_random_bytes(12)
        cipher = AES.new(wrapping_key, AES.MODE_GCM, nonce=nonce)
        wrapped_aes_key, tag = cipher.encrypt_and_digest(aes_key)

        metadata = {
            "kem_algorithm": self.kem_algorithm,
            "kem_ciphertext": self._b64_encode(kem_ciphertext),
            "secret_key": self._b64_encode(secret_key),  # POC only (not production-safe)
            "wrapped_aes_key": self._b64_encode(wrapped_aes_key),
            "wrap_nonce": self._b64_encode(nonce),
            "wrap_tag": self._b64_encode(tag),
        }

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)

        print("✅ Hybrid encryption complete.")
        print(f"   Encrypted file: {encrypted_file}")
        print(f"   Metadata file: {metadata_file}")

    # -------------------------
    # Decrypt
    # -------------------------

    def decrypt(self, encrypted_file: str, metadata_file: str, output_file: str) -> None:
        """
        Decrypt file using:
        - ML-KEM decapsulation to recover wrapping key
        - AES-GCM unwrap to recover AES file key
        - AES file decryption
        """

        print("📂 Loading metadata...")
        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        kem_ciphertext = self._b64_decode(metadata["kem_ciphertext"])
        secret_key = self._b64_decode(metadata["secret_key"])
        wrapped_aes_key = self._b64_decode(metadata["wrapped_aes_key"])
        nonce = self._b64_decode(metadata["wrap_nonce"])
        tag = self._b64_decode(metadata["wrap_tag"])

        print("🔓 Decapsulating shared secret...")
        shared_secret = decapsulate(
            kem_ciphertext,
            secret_key,
            metadata["kem_algorithm"],
        )

        wrapping_key = shared_secret[:32]

        print("🔑 Unwrapping AES key...")
        from Crypto.Cipher import AES

        cipher = AES.new(wrapping_key, AES.MODE_GCM, nonce=nonce)
        aes_key = cipher.decrypt_and_verify(wrapped_aes_key, tag)

        print("📄 Decrypting file...")
        decrypt_file(encrypted_file, output_file, aes_key)

        print("✅ Hybrid decryption complete.")
        print(f"   Decrypted file: {output_file}")