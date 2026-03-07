"""Hybrid pipeline tests for QuantumShield."""

from __future__ import annotations

import os
import tempfile

import pytest

from quantumshield.core.hybrid_engine import decrypt_file, encrypt_file
from quantumshield.core import kyber_module
from quantumshield.core.kyber_module import generate_keypair


def _skip_if_oqs_missing() -> None:
    if not kyber_module.is_oqs_available():
        pytest.skip("liboqs not available in this environment")


def _write_sample_file(path: str) -> bytes:
    payload = b"QuantumShield hybrid pipeline test payload"
    with open(path, "wb") as file_out:
        file_out.write(payload)
    return payload


def test_encrypt_creates_output() -> None:
    _skip_if_oqs_missing()
    public_key, _secret_key = generate_keypair()

    with tempfile.TemporaryDirectory() as tmpdir:
        plain_path = os.path.join(tmpdir, "plain.bin")
        enc_path = os.path.join(tmpdir, "enc.qs")
        _write_sample_file(plain_path)

        encrypt_file(plain_path, enc_path, public_key)

        assert os.path.exists(enc_path)
        assert os.path.getsize(enc_path) > 0


def test_encrypt_decrypt_round_trip() -> None:
    _skip_if_oqs_missing()
    public_key, secret_key = generate_keypair()

    with tempfile.TemporaryDirectory() as tmpdir:
        plain_path = os.path.join(tmpdir, "plain.bin")
        enc_path = os.path.join(tmpdir, "enc.qs")
        dec_path = os.path.join(tmpdir, "dec.bin")
        payload = _write_sample_file(plain_path)

        encrypt_file(plain_path, enc_path, public_key)
        decrypt_file(enc_path, dec_path, secret_key)

        with open(dec_path, "rb") as file_in:
            recovered = file_in.read()

        assert recovered == payload


def test_tampering_fails_authentication() -> None:
    _skip_if_oqs_missing()
    public_key, secret_key = generate_keypair()

    with tempfile.TemporaryDirectory() as tmpdir:
        plain_path = os.path.join(tmpdir, "plain.bin")
        enc_path = os.path.join(tmpdir, "enc.qs")
        dec_path = os.path.join(tmpdir, "dec.bin")
        _write_sample_file(plain_path)

        encrypt_file(plain_path, enc_path, public_key)

        with open(enc_path, "rb") as file_in:
            data = bytearray(file_in.read())

        data[-1] ^= 0x01

        with open(enc_path, "wb") as file_out:
            file_out.write(data)

        with pytest.raises(ValueError):
            decrypt_file(enc_path, dec_path, secret_key)


def test_wrong_key_fails_decryption() -> None:
    _skip_if_oqs_missing()
    public_key, _secret_key = generate_keypair()
    _other_public_key, other_secret_key = generate_keypair()

    with tempfile.TemporaryDirectory() as tmpdir:
        plain_path = os.path.join(tmpdir, "plain.bin")
        enc_path = os.path.join(tmpdir, "enc.qs")
        dec_path = os.path.join(tmpdir, "dec.bin")
        _write_sample_file(plain_path)

        encrypt_file(plain_path, enc_path, public_key)

        with pytest.raises(ValueError):
            decrypt_file(enc_path, dec_path, other_secret_key)
