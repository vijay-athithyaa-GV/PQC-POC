# QuantumShield

Proof of concept for a crypto-agile hybrid cryptographic architecture resistant to quantum attacks.

## What is implemented (Day 1-3)

- AES-256-GCM byte encryption/decryption
- AES-256-GCM file encryption/decryption
- ML-KEM (Kyber) key encapsulation using liboqs-python (standalone)

## Requirements

- Ubuntu
- Python 3.10+
- liboqs
- liboqs-python
- pycryptodome

## Setup

1) Create and activate a virtual environment:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## AES file demo

Prepare an input file (example):

```bash
echo "QuantumShield demo file" > sample.txt
```

Run the file-based demo:

```bash
python -m quantumshield.tests.run_aes_file_demo sample.txt sample.enc sample.dec.txt
```

- sample.txt must exist (input)
- sample.enc and sample.dec.txt are created by the script

## Kyber demo (ML-KEM)

```bash
python - <<'PY'
from quantumshield.core.kyber_module import generate_keypair, encapsulate, decapsulate

public_key, secret_key = generate_keypair()
ciphertext, shared_secret_1 = encapsulate(public_key)
shared_secret_2 = decapsulate(ciphertext, secret_key)

print("Shared secrets match:", shared_secret_1 == shared_secret_2)
PY
```

## Project layout

```
quantumshield/
├── core/
│   ├── aes_module.py
│   ├── kyber_module.py
│   ├── hybrid_engine.py
│   └── crypto_agility.py
├── cli/
│   └── main.py
├── tests/
└── benchmarks/
```

## Notes

- Hybrid integration (Kyber + AES) is not implemented yet.
- This is a proof of concept intended for learning and experimentation.

## Day 4 – Hybrid Integration (Key Wrapping Layer)

- Integrated ML-KEM (Kyber) with AES-256-GCM

- Implemented secure AES key wrapping using ML-KEM shared secret

- Base64-safe metadata packaging for binary components

- Proper nonce and authentication tag storage for AES-GCM

- Crypto-agile structure allowing KEM algorithm selection

## Architecture introduced:

    File → AES-256-GCM encryption
    AES key → Wrapped using ML-KEM shared secret
    ML-KEM ciphertext + wrapped key → Stored in metadata.json
## Day 5 – Full Hybrid Encryption Engine

- Implemented HybridEngine class

- End-to-end file encryption & decryption

- ML-KEM-768 protecting AES file encryption key

- Clean separation between:

    File encryption layer (AES)

    Key encapsulation layer (ML-KEM)

- Verified integrity using AES-GCM authentication

# Result:
- Fully functional post-quantum hybrid file encryption system.

## Hybrid Encryption Demo

    Prepare an input file:

    echo "Quantum Test File" > test.txt

    Run hybrid encryption:

    python - <<'PY'
    from quantumshield.core.hybrid_engine import HybridEngine

    engine = HybridEngine()

    engine.encrypt("test.txt", "encrypted.bin", "metadata.json")
    engine.decrypt("encrypted.bin", "metadata.json", "decrypted.txt")
    PY

    Expected output:

    Hybrid encryption complete.
    Hybrid decryption complete.

    Verify result:

    cat decrypted.txt

    Output:

    Quantum Test File
## Hybrid Architecture Overview
QuantumShield now implements a hybrid post-quantum encryption model:

AES-256-GCM encrypts file contents

ML-KEM encapsulates a shared secret

Shared secret derives a wrapping key

AES file key is encrypted using wrapping key

Metadata stores:

ML-KEM ciphertext

Wrapped AES key

GCM nonce and authentication tag

This follows modern hybrid cryptographic design principles.

## Security Notes

This is a Proof-of-Concept implementation.

Secret keys are stored in metadata for testing purposes.

In a production system:

Receiver generates ML-KEM keypair.

Sender uses receiver's public key.

Secret keys must never be transmitted or stored alongside ciphertext.

Not audited for production security.

## Updated Project Layout
    quantumshield/
    ├── core/
    │   ├── aes_module.py
    │   ├── kyber_module.py
    │   ├── hybrid_engine.py
    │   └── crypto_agility.py
    ├── cli/
    │   └── main.py
    ├── tests/
    ├── benchmarks/
    └── README.md
