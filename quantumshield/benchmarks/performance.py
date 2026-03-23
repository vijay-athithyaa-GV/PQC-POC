"""Performance benchmarks for AES, Kyber, and full pipeline."""

from __future__ import annotations

import os
import tempfile
import time
from typing import Iterable, Tuple

from Crypto.Random import get_random_bytes

from quantumshield.core import aes_module, kyber_module
from quantumshield.core.hybrid_engine import decrypt_file, encrypt_file


def _timeit(fn) -> Tuple[float, object]:
    start = time.perf_counter()
    result = fn()
    end = time.perf_counter()
    return end - start, result


def _format_seconds(seconds: float) -> str:
    return f"{seconds:.6f}"


def _bench_aes_sizes(sizes: Iterable[int]) -> None:
    print("AES-256-GCM encryption time by size")
    print("-----------------------------------")
    for size in sizes:
        key = aes_module.generate_aes_key()
        payload = get_random_bytes(size)
        elapsed, _ = _timeit(lambda: aes_module.encrypt_bytes(payload, key))
        print(f"{size:>8} bytes: {_format_seconds(elapsed)}")
    print("")


def _bench_kyber() -> None:
    print("Kyber encapsulation time")
    print("------------------------")
    if not kyber_module.is_oqs_available():
        print("liboqs not available, skipping")
        print("")
        return

    public_key, secret_key = kyber_module.generate_keypair()
    enc_time, enc_data = _timeit(lambda: kyber_module.encapsulate(public_key))
    ciphertext, _shared_secret = enc_data
    dec_time, _ = _timeit(lambda: kyber_module.decapsulate(ciphertext, secret_key))

    print(f"Encapsulate: {_format_seconds(enc_time)}")
    print(f"Decapsulate: {_format_seconds(dec_time)}")
    print("")


def _bench_pipeline(payload_size: int) -> None:
    print("Full hybrid pipeline time")
    print("-------------------------")
    if not kyber_module.is_oqs_available():
        print("liboqs not available, skipping")
        print("")
        return

    public_key, secret_key = kyber_module.generate_keypair()

    with tempfile.TemporaryDirectory() as tmpdir:
        plain_path = os.path.join(tmpdir, "plain.bin")
        enc_path = os.path.join(tmpdir, "enc.qs")
        dec_path = os.path.join(tmpdir, "dec.bin")

        with open(plain_path, "wb") as file_out:
            file_out.write(get_random_bytes(payload_size))

        enc_time, _ = _timeit(lambda: encrypt_file(plain_path, enc_path, public_key))
        dec_time, _ = _timeit(lambda: decrypt_file(enc_path, dec_path, secret_key))

    print(f"Encrypt file: {_format_seconds(enc_time)}")
    print(f"Decrypt file: {_format_seconds(dec_time)}")
    print("")


def main() -> None:
    _bench_aes_sizes([1024, 1024 * 10, 1024 * 100, 1024 * 1024])
    _bench_kyber()
    _bench_pipeline(1024 * 1024)


if __name__ == "__main__":
    main()
