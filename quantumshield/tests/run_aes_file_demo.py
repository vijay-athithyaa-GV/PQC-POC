"""File-based AES-GCM demo for simple encryption/decryption."""

from __future__ import annotations

import sys

from quantumshield.core.aes_module import decrypt_file, encrypt_file


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: python -m quantumshield.tests.run_aes_file_demo <in> <enc> <dec>")
        return 1

    input_path, enc_path, dec_path = sys.argv[1:4]
    key = encrypt_file(input_path, enc_path)
    decrypt_file(enc_path, dec_path, key)
    print("OK: decrypted file written to", dec_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
