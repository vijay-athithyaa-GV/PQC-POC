"""Benchmark RSA-wrapped AES key vs Kyber KEM.

Day 10 comparison module.
"""

from __future__ import annotations

import time
from typing import Tuple

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from quantumshield.core import kyber_module

AES_KEY_SIZE_BYTES = 32
RSA_KEY_SIZE_BITS = 2048


def _timeit(fn) -> Tuple[float, object]:
    start = time.perf_counter()
    result = fn()
    end = time.perf_counter()
    return end - start, result


def _rsa_round_trip(aes_key: bytes) -> Tuple[float, float, float]:
    gen_time, keypair = _timeit(lambda: RSA.generate(RSA_KEY_SIZE_BITS))
    public_key = keypair.publickey()

    encrypt_time, enc_key = _timeit(
        lambda: PKCS1_OAEP.new(public_key).encrypt(aes_key)
    )
    decrypt_time, _ = _timeit(lambda: PKCS1_OAEP.new(keypair).decrypt(enc_key))

    return gen_time, encrypt_time, decrypt_time


def _kyber_round_trip() -> Tuple[float, float, float]:
    gen_time, keypair = _timeit(kyber_module.generate_keypair)
    public_key, secret_key = keypair

    encrypt_time, kem_data = _timeit(lambda: kyber_module.encapsulate(public_key))
    ciphertext, _shared_secret = kem_data
    decrypt_time, _ = _timeit(
        lambda: kyber_module.decapsulate(ciphertext, secret_key)
    )

    return gen_time, encrypt_time, decrypt_time


def main() -> None:
    aes_key = get_random_bytes(AES_KEY_SIZE_BYTES)

    rsa_gen, rsa_enc, rsa_dec = _rsa_round_trip(aes_key)

    if kyber_module.is_oqs_available():
        kyber_gen, kyber_enc, kyber_dec = _kyber_round_trip()
    else:
        kyber_gen = kyber_enc = kyber_dec = None

    print("RSA vs Kyber (time in seconds)")
    print("--------------------------------")
    print(f"RSA keygen: {rsa_gen:.6f}")
    print(f"RSA encrypt (AES key): {rsa_enc:.6f}")
    print(f"RSA decrypt (AES key): {rsa_dec:.6f}")

    if kyber_gen is None:
        print("Kyber results: liboqs not available")
    else:
        print(f"Kyber keygen: {kyber_gen:.6f}")
        print(f"Kyber encapsulate: {kyber_enc:.6f}")
        print(f"Kyber decapsulate: {kyber_dec:.6f}")


if __name__ == "__main__":
    main()
