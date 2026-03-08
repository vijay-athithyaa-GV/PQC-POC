import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.hybrid_engine import encrypt_file, decrypt_file
from core.kyber_module import generate_keypair


def main():
    parser = argparse.ArgumentParser(description="QuantumShield CLI Tool")

    subparsers = parser.add_subparsers(dest="command")

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("input_file")
    encrypt_parser.add_argument("output_file")

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("input_file")
    decrypt_parser.add_argument("output_file")

    args = parser.parse_args()

    if args.command == "encrypt":

        public_key, secret_key = generate_keypair()

        encrypt_file(args.input_file, args.output_file, public_key)

        with open("secret.key", "wb") as f:
            f.write(secret_key)

        print("Encryption successful")
        print("Secret key saved to secret.key")

    elif args.command == "decrypt":

        with open("secret.key", "rb") as f:
            secret_key = f.read()

        decrypt_file(args.input_file, args.output_file, secret_key)

        print("Decryption successful")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
