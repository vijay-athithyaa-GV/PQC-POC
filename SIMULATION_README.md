# QuantumShield - Frontend/Backend Crypto Simulation

##  What's Implemented

A **real-time encryption/decryption web simulation** with:

- **Flask Backend API** (`app.py`) - Provides REST endpoints for:
  - Key generation (Kyber ML-KEM-768)
  - Encryption (Kyber + AES-256-GCM hybrid)
  - Decryption (with verification)
  - File encryption support

- **Interactive Web UI** (`templates/index.html`) - Beautiful dashboard showing:
  - Live encryption/decryption visualization
  - Key management interface
  - Real-time statistics and metrics
  - Data visualization with Base64 outputs
  - Ciphertext and key inspection

- **Command-line Test Suite** (`test_simulation.py`) - For automated testing and demonstration

##  Running the Simulation - Step by Step

### **STEP 1: Open a Terminal**
```bash
# Use WSL Ubuntu terminal or Linux terminal
# Navigate to the project directory
cd /home/shiva/PQC-POC
```

### **STEP 2: Create Virtual Environment (First Time Only)**
```bash
# Create a virtual environment
python3 -m venv venv_simulator

# Activate the virtual environment
source venv_simulator/bin/activate
```

After activation, you should see `(venv_simulator)` prefix in your terminal.

### **STEP 3: Install Dependencies**
```bash
# Install all required packages
pip install -q flask flask-cors pycryptodome liboqs-python requests
```

Wait for installation to complete (takes a few minutes for liboqs-python).

### **STEP 4: Set Environment Variables**
```bash
# These are needed for liboqs-python to work
export OQS_INSTALL_DIR=$HOME/.local
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
```

### **STEP 5: Choose Your Simulation Method**

#### **Option A: Web Interface (Interactive) - RECOMMENDED**

```bash
# Start the Flask backend
python3 app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Then:
1. **Open your browser** → Go to: `http://localhost:5000`
2. **Click "Generate Keys"** → See Kyber keypair generated
3. **Enter text** in the plaintext box (or use default text)
4. **Click "Encrypt"** → See ciphertext and statistics
5. **Click "Decrypt Last Ciphertext"** → See original message recovered with ✓ MATCH

#### **Option B: Command-Line Test (Automated)**

In a **new terminal**, run:
```bash
cd /home/shiva/PQC-POC
source venv_simulator/bin/activate
export OQS_INSTALL_DIR=$HOME/.local
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
python3 test_simulation.py
```

This will automatically:
- Generate keys
- Encrypt a test message
- Decrypt the message
- Verify perfect recovery
- Display encryption statistics

Expected successful output:
```
✓ Keygeneration: SUCCESS
✓ Encryption: SUCCESS  
✓ Decryption: SUCCESS
✓ PERFECT MATCH: Original and decrypted messages are identical
✓ Data integrity verified with GCM authentication tag
```

---

##  Copy-Paste Commands

**For fastest setup, copy and paste these commands:**

### **Terminal 1: Start Backend Server**
```bash
cd /home/shiva/PQC-POC && source venv_simulator/bin/activate && export OQS_INSTALL_DIR=$HOME/.local && export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH && python3 app.py
```

Then open browser: `http://localhost:5000`

### **Or Terminal 1: Run Automated Test**
```bash
cd /home/shiva/PQC-POC && source venv_simulator/bin/activate && export OQS_INSTALL_DIR=$HOME/.local && export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH && python3 test_simulation.py
```

---

##  Quick Start

### 1. Set up and run the Flask backend:

```bash
cd /home/shiva/PQC-POC

# Create and activate virtual environment
python3 -m venv venv_simulator
source venv_simulator/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
export OQS_INSTALL_DIR=$HOME/.local
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
python3 app.py
```

The Flask server will start at `http://localhost:5000`

### 2. Access the web interface:

Open your browser and go to: **http://localhost:5000**

### 3. Or run the automated test:

```bash
source venv_simulator/bin/activate
python3 test_simulation.py
```
```

##  Complete Workflow Example - What to Expect

### **Web Interface Workflow:**

```
START
  ↓
[Step 1] Open Browser at http://localhost:5000
  ↓
[Step 2] Click "Generate Keys" Button
  Status Message: "✓ Keys generated successfully!"
  Display: Public Key (Base64), Sizes
  ↓
[Step 3] Enter Message (or keep default)
  Input: "Hello, QuantumShield! This is a secure message..."
  ↓
[Step 4] Click "Encrypt" Button
  Process:
    • Kyber encapsulation → Shared secret generated
    • AES-256-GCM encryption → Ciphertext created
  Status Message: "✓ Encryption successful! 🔐"
  Display: Ciphertext, KEM Ciphertext, Statistics
  ↓
[Step 5] Click "Decrypt Last Ciphertext" Button
  Process:
    • Kyber decapsulation → Secret recovered
    • AES-256-GCM decryption → Message recovered
    • GCM verification → Tag validated
  Status Message: "✓ Decryption successful! 🔓"
  Display: Decrypted message, "✅ MATCH" verification
  ↓
SUCCESS ✓
Original Message = Decrypted Message
```

### **Expected Statistics Display:**

```
Key Management:
  • Public Key Size: 1184 bytes (ML-KEM-768 standard)
  • Secret Key Size: 2400 bytes

Encryption:
  • Plaintext Size: 79 bytes
  • Ciphertext Size: 79 bytes
  • KEM Ciphertext Size: 1088 bytes
  • Total Encrypted Size: 1195 bytes
  • Shared Secret Size: 32 bytes

Decryption:
  • Decrypted Size: 79 bytes
  • Verification Status: ✅ PERFECT MATCH
```

---

##  Architecture

```
┌─────────────────────────────────────────┐
│       Web Frontend (HTML/JS)            │
│  • Key Management UI                    │
│  • Text Encryption Form                 │
│  • Real-time Decryption Display        │
│  • Statistics Dashboard                 │
└─────────────┬───────────────────────────┘
              │ HTTP/JSON
              ▼
┌─────────────────────────────────────────┐
│       Flask Backend (Python)            │
│  • /api/generate-keys                   │
│  • /api/encrypt                         │
│  • /api/decrypt                         │
│  • /api/encrypt-file (bonus)           │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│    QuantumShield Crypto Core            │
│  • Kyber ML-KEM-768 (Key Encapsulation)│
│  • AES-256-GCM (Symmetric Encryption)   │
│  • Hybrid Pipeline                      │
└─────────────────────────────────────────┘
```

##  Encryption Flow Visualization

### Encryption Process:
```
Plaintext
    ↓
[1] Kyber Encapsulation
    → Generates: KEM Ciphertext, Shared Secret
    ↓
[2] AES-256-GCM Encryption
    → Input: Plaintext + AES Key (from shared secret)
    → Output: Ciphertext, Nonce, Authentication Tag
    ↓
Combined Package:
  - KEM Ciphertext (1088 bytes)
  - Ciphertext (variable)
  - Nonce (12 bytes)
  - Tag (16 bytes)
```

### Decryption Process:
```
Encrypted Package
    ↓
[1] Kyber Decapsulation
    → Input: KEM Ciphertext + Secret Key
    → Output: Recovered Shared Secret
    ↓
[2] AES-256-GCM Decryption
    → Input: Ciphertext + AES Key + Nonce + Tag
    → Verification: Tag authentication check
    → Output: Plaintext
    ↓
Original Message Recovered ✓
```

##  Demonstration Results

From the test run:
```
✓ Keygeneration: SUCCESS
  • Public Key: 1184 bytes (ML-KEM-768)
  • Secret Key: 2400 bytes

✓ Encryption: SUCCESS
  • Original Message: 79 bytes
  • KEM Ciphertext: 1088 bytes
  • Encrypted Message: 79 bytes
  • Total Overhead: 1195 bytes

✓ Decryption: SUCCESS
  • Recovered Message: 79 bytes
  • ✓ PERFECT MATCH with original
  • ✓ GCM Authentication VERIFIED
```

##  Features

### Web UI Features:
- Generate quantum-resistant keypairs
- Encrypt text messages in real-time
- Decrypt with automatic verification
- View ciphertext and key components
- Copy-to-clipboard functionality
- Live statistics and metrics
- Responsive design (desktop/mobile)
- Dark gradient theme

### API Endpoints:
```
POST /api/generate-keys
  → Returns: public_key, secret_key (Base64)

POST /api/encrypt
  Body: { plaintext: "message" }
  → Returns: ciphertext, kem_ciphertext, nonce, tag, aes_key

POST /api/decrypt
  Body: { kem_ciphertext, ciphertext, nonce, tag }
  → Returns: plaintext, verification status

POST /api/encrypt-file
  Upload file to encrypt
  → Returns: encrypted file data
```

##  Security Highlights

1. **Post-Quantum Safe**: Uses Kyber ML-KEM-768 (NIST-standardized)
2. **Strong Encryption**: AES-256-GCM with authenticated encryption
3. **Perfect Integrity**: GCM authentication tag prevents tampering
4. **Secure Key Derivation**: Shared secret properly truncated to 32 bytes

## File Structure

```
PQC-POC/
├── app.py                          # Flask backend
├── test_simulation.py              # Command-line test
├── templates/
│   └── index.html                 # Web UI
├── quantumshield/
│   └── core/
│       ├── hybrid_engine.py       # Encryption pipeline
│       ├── aes_module.py          # AES-256-GCM
│       └── kyber_module.py        # Kyber ML-KEM
└── requirements.txt
```

##  Testing

Run automated tests:
```bash
source venv_simulator/bin/activate
python3 test_simulation.py
```

Expected output:
- ✓ Keygeneration successful
- ✓ Encryption successful
- ✓ Decryption successful
- ✓ Perfect message match
- ✓ GCM authentication verified

##  Web UI Preview

The web interface provides:
- **Left Panel**: Key Management
- **Right Panel**: Encryption
- **Bottom Panel**: Decryption & Verification
- **Real-time Statistics**: Size metrics and performance
- **Flow Diagrams**: Visual representation of crypto operations

##  Usage Examples

### Example 1: Default encryption
```
plaintext: "Hello, QuantumShield! This is a secure message."
1. Click "Generate Keys"
2. Click "Encrypt"
3. View ciphertext and statistics
4. Click "Decrypt Last Ciphertext"
5. See original message recovered with ✓ MATCH
```

### Example 2: Long messages
Encrypt large messages (tested with 1000+ characters):
```
plaintext: "Very long text..." (1000+ bytes)
- Works seamlessly
- AES-256-GCM scales efficiently
- Decryption always perfect
```

## Troubleshooting

### Issue: Port 5000 already in use
```bash
# Kill the process using port 5000
lsof -ti:5000 | xargs kill -9
# Or use a different port (modify app.py)
```

### Issue: liboqs not found
```bash
# Ensure environment variables are set
export OQS_INSTALL_DIR=$HOME/.local
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
```

### Issue: CORS errors in frontend
Already configured with `flask-cors`, should not occur.

## References

- **Kyber ML-KEM**: ML-KEM: Module-Lattice-Based Key-Encapsulation Mechanism
- **AES-256-GCM**: Advanced Encryption Standard with Galois/Counter Mode
- **NIST PQC**: Post-Quantum Cryptography Standardization
- **liboqs-python**: Open Quantum Safe Python Bindings

## Status

✓ Backend API: **WORKING**
✓ Encryption: **WORKING**
✓ Decryption: **WORKING**
✓ Verification: **WORKING**
✓ Web UI: **READY**
✓ Test Suite: **WORKING**

---

**Ready to encrypt and decrypt in real-time!**
