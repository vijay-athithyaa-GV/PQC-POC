#!/usr/bin/env python3
"""Test script for QuantumShield simulation API."""

import sys
import time
import subprocess
import requests
import json
from typing import Dict, Any

API_BASE = 'http://localhost:5000/api'

def make_request(endpoint: str, method: str = 'POST', data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make API request."""
    url = f"{API_BASE}/{endpoint}"
    try:
        if method == 'POST':
            response = requests.post(url, json=data or {}, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {'status': 'error', 'message': 'Cannot connect to server'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def print_header(text: str):
    """Print formatted header."""
    width = 80
    print("\n" + "=" * width)
    print(f"  {text}".ljust(width - 2))
    print("=" * width + "\n")

def print_section(text: str):
    """Print section header."""
    print(f"\n▶ {text}")
    print("-" * 70)

def test_encryption_demo():
    """Demonstrate encryption and decryption."""
    print_header("🔐 QuantumShield Hybrid Encryption Demonstration")
    
    # Step 1: Generate Keys
    print_section("Step 1: Generate Kyber Keypair (ML-KEM-768)")
    print("Generating quantum-resistant keypair...")
    response = make_request('generate-keys')
    
    if response['status'] != 'success':
        print(f"ERROR: {response['message']}")
        return
    
    print(f"✓ Keypair generated successfully")
    print(f"  • Public Key Size: {response['public_key_size']} bytes")
    print(f"  • Secret Key Size: {response['secret_key_size']} bytes")
    print(f"  • Public Key (first 50 chars): {response['public_key'][:50]}...")
    
    public_key = response['public_key']
    
    # Step 2: Encrypt Text
    print_section("Step 2: Encrypt Message with Hybrid Pipeline")
    plaintext = "Hello, QuantumShield! This is a secure message using post-quantum cryptography."
    print(f"Original Message: \"{plaintext}\"")
    print(f"Message Size: {len(plaintext)} bytes")
    print("\nEncrypting with Kyber + AES-256-GCM...")
    
    response = make_request('encrypt', data={'plaintext': plaintext})
    
    if response['status'] != 'success':
        print(f"ERROR: {response['message']}")
        return
    
    print(f"✓ Encryption successful")
    print(f"\n  Encryption Process:")
    print(f"  1. Kyber Encapsulation of Shared Secret")
    print(f"     → KEM Ciphertext Size: {response['kem_ciphertext_size']} bytes")
    print(f"     → Shared Secret Size: {response['shared_secret_size']} bytes")
    print(f"  2. AES-256-GCM Encryption of Message")
    print(f"     → Plaintext Size: {response['plaintext_size']} bytes")
    print(f"     → Ciphertext Size: {response['ciphertext_size']} bytes")
    print(f"  3. Encapsulation Metadata")
    print(f"     → Nonce (GCM): 12 bytes")
    print(f"     → Authentication Tag: 16 bytes")
    
    print(f"\n  Output (Ciphertext - first 80 chars):")
    print(f"  {response['ciphertext'][:80]}...")
    print(f"\n  Output (KEM Ciphertext - first 80 chars):")
    print(f"  {response['kem_ciphertext'][:80]}...")
    
    # Store for decryption
    kem_ciphertext = response['kem_ciphertext']
    ciphertext = response['ciphertext']
    nonce = response['nonce']
    tag = response['tag']
    
    # Step 3: Decrypt
    print_section("Step 3: Decrypt Message with Hybrid Pipeline")
    print("Preparing to decrypt using secret key...")
    print("\nDecrypting with Kyber + AES-256-GCM...")
    
    response = make_request('decrypt', data={
        'kem_ciphertext': kem_ciphertext,
        'ciphertext': ciphertext,
        'nonce': nonce,
        'tag': tag,
    })
    
    if response['status'] != 'success':
        print(f"ERROR: {response['message']}")
        return
    
    print(f"✓ Decryption successful")
    print(f"\n  Decryption Process:")
    print(f"  1. Kyber Decapsulation to recover Shared Secret")
    print(f"     → Shared Secret Size: {response['shared_secret_size']} bytes")
    print(f"  2. AES-256-GCM Decryption")
    print(f"     → Decrypted Size: {response['plaintext_size']} bytes")
    print(f"\n  Decrypted Message: \"{response['plaintext']}\"")
    
    # Verification
    print_section("Step 4: Verification")
    if response['plaintext'] == plaintext:
        print("✓ PERFECT MATCH: Original and decrypted messages are identical")
        print("✓ Data integrity verified with GCM authentication tag")
    else:
        print("✗ MISMATCH: Messages do not match!")
    
    # Summary
    print_header("📊 Encryption Statistics Summary")
    print(f"{'Metric':<40} {'Value':>20}")
    print("-" * 61)
    
    encrypt_response = make_request('encrypt', data={'plaintext': plaintext})
    kem_size = encrypt_response.get('kem_ciphertext_size', 0)
    cipher_size = encrypt_response.get('ciphertext_size', 0)
    
    print(f"{'Original Message Size':<40} {len(plaintext):>20} bytes")
    print(f"{'Ciphertext Size':<40} {cipher_size:>20} bytes")
    print(f"{'KEM Ciphertext Size':<40} {kem_size:>20} bytes")
    print(f"{'Total Encrypted Size':<40} {kem_size + cipher_size + 12 + 16:>20} bytes")
    print(f"{'Shared Secret Size':<40} {response['shared_secret_size']:>20} bytes")
    print("-" * 61)
    
    if cipher_size > 0:
        expansion = ((kem_size + cipher_size + 12 + 16) / len(plaintext)) * 100
        print(f"{'Ciphertext Expansion':<40} {expansion:>19.1f}%")
    
    print("\n✓ Demonstration completed successfully!")
    print("\nKey Highlights:")
    print("  • Kyber ML-KEM-768: Post-quantum key encapsulation")
    print("  • AES-256-GCM: 256-bit authenticated encryption")
    print("  • Hybrid approach: Quantum-resistant + symmetric encryption")
    print("  • Data integrity: GCM authentication tag verified")

if __name__ == '__main__':
    print("\n🚀 QuantumShield Encryption/Decryption Test Suite")
    print("Waiting for Flask server to be ready...\n")
    
    # Wait for server to be ready
    max_attempts = 30
    for i in range(max_attempts):
        try:
            response = requests.get(f'{API_BASE}/../', timeout=2)
            print("✓ API server is ready!")
            break
        except:
            if i < max_attempts - 1:
                time.sleep(1)
                print(".", end="", flush=True)
            else:
                print("\n✗ Could not connect to API server at http://localhost:5000")
                print("\nMake sure to run the Flask app with:")
                print("  source venv_simulator/bin/activate")
                print("  python3 app.py")
                sys.exit(1)
    
    # Run the test
    try:
        test_encryption_demo()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        sys.exit(1)
