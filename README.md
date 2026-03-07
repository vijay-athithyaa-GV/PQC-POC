# QuantumShield

Proof of concept for a crypto-agile hybrid cryptographic architecture resistant to quantum attacks.

## What is implemented (Day 1-7)

- AES-256-GCM byte encryption/decryption
- AES-256-GCM file encryption/decryption
- ML-KEM (Kyber) key encapsulation using liboqs-python
- Encrypted file packaging format (binary container)
- Full hybrid encryption pipeline (Kyber + AES-GCM)

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

3) Install liboqs with shared libraries (required by liboqs-python):

```bash
cd ~
git clone https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir build && cd build
cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=$HOME/.local ..
make -j$(nproc)
make install
```

4) Ensure the loader can find liboqs:

```bash
export OQS_INSTALL_DIR=$HOME/.local
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
```
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
│   ├── package_format.py
│   └── hybrid_engine.py
├── cli/
│   └── main.py
├── tests/
└── benchmarks/
```

## Notes

- This is a proof of concept intended for learning and experimentation.
- Hybrid encryption requires a working liboqs shared library.

## Day 6 – Encrypted File Packaging Format

Binary container format:

```
[ MAGIC HEADER (7 bytes) : b"QSHIELD" ]
[ VERSION (1 byte) ]
[ KYBER_CIPHERTEXT_LENGTH (4 bytes big endian) ]
[ KYBER_CIPHERTEXT (variable length) ]
[ AES_NONCE (12 bytes) ]
[ AES_TAG (16 bytes) ]
[ AES_CIPHERTEXT (remaining bytes) ]
```

## Day 7 – Full Hybrid Encryption Pipeline

- Kyber encapsulates a shared secret
- AES-256-GCM key is derived from the shared secret
- Encrypted data is packaged using the binary container

## Hybrid Encryption Demo

Prepare an input file:

```bash
echo "Quantum Test File" > test.txt
```

Run hybrid encryption:

```bash
python - <<'PY'
from quantumshield.core.hybrid_engine import decrypt_file, encrypt_file
from quantumshield.core.kyber_module import generate_keypair

public_key, secret_key = generate_keypair()
encrypt_file("test.txt", "encrypted.qs", public_key)
decrypt_file("encrypted.qs", "decrypted.txt", secret_key)
PY
```

Verify result:

```bash
cat decrypted.txt
```

## Testing

Disable external pytest plugins (recommended on ROS-based systems):

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q
```

Run only the hybrid pipeline tests:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -q quantumshield/tests/test_pipeline.py
```

## Security Notes

This is a proof-of-concept implementation and is not audited.
