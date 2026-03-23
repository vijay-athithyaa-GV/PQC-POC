# QuantumShield Final Report (Day 14)

## Architecture Diagram (Text)

[Input File]
    |
    v
[Hybrid Engine]
    |-- Kyber KEM -> shared secret
    |-- AES-256-GCM -> ciphertext, nonce, tag
    v
[Package Format]
    |
    v
[Encrypted Container]

## Workflow Explanation
1. Generate a Kyber keypair (public and secret keys).
2. Encrypt a file with AES-256-GCM using a key derived from Kyber encapsulation.
3. Package the Kyber ciphertext with AES nonce, tag, and ciphertext.
4. Decrypt by parsing the package, decapsulating the shared secret, and validating AES-GCM.

## Module Descriptions
- core/aes_module.py: AES-256-GCM encrypt/decrypt utilities for bytes and files.
- core/kyber_module.py: ML-KEM (Kyber) key encapsulation wrapper for liboqs.
- core/crypto_agility.py: Interface layer for symmetric ciphers and KEMs.
- core/hybrid_engine.py: Orchestrates the hybrid flow and packaging.
- core/package_format.py: Defines the binary container format.
- cli/main.py: Command-line interface for keygen, encrypt, decrypt.

## Security Features
- AES-256-GCM authentication for tamper detection.
- Kyber KEM for post-quantum key exchange.
- Package format validation for structural integrity.
- Input validation and error handling in the hybrid pipeline.
- Secret key file is created with restricted permissions.

## Benchmarking Results
Run the following to populate results:
- python -m quantumshield.benchmarks.rsa_vs_kyber
- python -m quantumshield.benchmarks.performance

Record the output here after running benchmarks.

## Usage Instructions
Key generation:
- python -m quantumshield.cli.main keygen

Encrypt:
- python -m quantumshield.cli.main encrypt input.txt output.qs

Decrypt:
- python -m quantumshield.cli.main decrypt output.qs output.txt

## Demo Steps
1. Generate keys:
   python -m quantumshield.cli.main keygen
2. Encrypt a file:
   python -m quantumshield.cli.main encrypt sample.txt sample.qs
3. Decrypt the file:
   python -m quantumshield.cli.main decrypt sample.qs sample.dec.txt
4. Verify output:
   cat sample.dec.txt
