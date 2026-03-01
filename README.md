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
