import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.hybrid_engine import decrypt_pipeline, encrypt_pipeline
from core.kyber_module import generate_keypair


def _write_secret_key(path: str, secret_key: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "wb") as file_out:
            file_out.write(secret_key)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def main():
    parser = argparse.ArgumentParser(description="QuantumShield CLI Tool")

    subparsers = parser.add_subparsers(dest="command")

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("input_file")
    encrypt_parser.add_argument("output_file")
    encrypt_parser.add_argument(
        "--public-key",
        dest="public_key_path",
        default="public.key",
        help="Path to Kyber public key file (default: public.key)",
    )
    encrypt_parser.add_argument(
        "--secret-key",
        dest="secret_key_path",
        default="secret.key",
        help="Path to Kyber secret key file (default: secret.key)",
    )

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("input_file")
    decrypt_parser.add_argument("output_file")
    decrypt_parser.add_argument(
        "--secret-key",
        dest="secret_key_path",
        default="secret.key",
        help="Path to Kyber secret key file (default: secret.key)",
    )

    keygen_parser = subparsers.add_parser("keygen", help="Generate a Kyber keypair")
    keygen_parser.add_argument(
        "--public-key",
        dest="public_key_path",
        default="public.key",
        help="Path to write public key (default: public.key)",
    )
    keygen_parser.add_argument(
        "--secret-key",
        dest="secret_key_path",
        default="secret.key",
        help="Path to write secret key (default: secret.key)",
    )

    args = parser.parse_args()

    try:
        if args.command == "encrypt":
            if not os.path.exists(args.public_key_path):
                raise FileNotFoundError(
                    f"public key not found: {args.public_key_path}. Run keygen first."
                )

            with open(args.public_key_path, "rb") as file_in:
                public_key = file_in.read()

            encrypt_pipeline(args.input_file, args.output_file, public_key)

            print("Encryption successful")
            print(f"Output written to {args.output_file}")

        elif args.command == "decrypt":
            if not os.path.exists(args.secret_key_path):
                raise FileNotFoundError(
                    f"secret key not found: {args.secret_key_path}. Run keygen first."
                )

            with open(args.secret_key_path, "rb") as file_in:
                secret_key = file_in.read()

            decrypt_pipeline(args.input_file, args.output_file, secret_key)

            print("Decryption successful")
            print(f"Output written to {args.output_file}")

        elif args.command == "keygen":
            public_key, secret_key = generate_keypair()

            with open(args.public_key_path, "wb") as file_out:
                file_out.write(public_key)

            _write_secret_key(args.secret_key_path, secret_key)

            print("Key generation successful")
            print(f"Public key saved to {args.public_key_path}")
            print(f"Secret key saved to {args.secret_key_path}")

        else:
            parser.print_help()
            return
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
