"""Minimal AES file encryption round-trip test."""

from __future__ import annotations

import os
import tempfile

from quantumshield.core.aes_module import decrypt_file, encrypt_file


def run_round_trip() -> None:
    payload = b"QuantumShield AES-GCM test payload"

    with tempfile.TemporaryDirectory() as tmpdir:
        plain_path = os.path.join(tmpdir, "plain.bin")
        enc_path = os.path.join(tmpdir, "enc.bin")
        dec_path = os.path.join(tmpdir, "dec.bin")

        with open(plain_path, "wb") as file_out:
            file_out.write(payload)

        key = encrypt_file(plain_path, enc_path)
        decrypt_file(enc_path, dec_path, key)

        with open(dec_path, "rb") as file_in:
            recovered = file_in.read()

    assert recovered == payload, "decrypted payload does not match"
    print("AES-GCM file round-trip OK")


if __name__ == "__main__":
    run_round_trip()
