"""Flask backend for QuantumShield crypto simulation."""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import base64
import json
import os
import sys

# Add quantumshield to path
sys.path.insert(0, os.path.dirname(__file__))

from quantumshield.core.hybrid_engine import encrypt_file, decrypt_file
from quantumshield.core.aes_module import encrypt_bytes, decrypt_bytes
from quantumshield.core.kyber_module import generate_keypair, encapsulate, decapsulate

app = Flask(__name__)
CORS(app)

# Store session keys
session_data = {
    'public_key': None,
    'secret_key': None,
    'last_ciphertext': None,
}


def bytes_to_b64(data):
    """Convert bytes to base64 string."""
    return base64.b64encode(data).decode('utf-8')


def b64_to_bytes(data):
    """Convert base64 string to bytes."""
    return base64.b64decode(data.encode('utf-8'))


@app.route('/')
def index():
    """Serve the frontend."""
    return render_template('index.html')


@app.route('/api/generate-keys', methods=['POST'])
def generate_keys():
    """Generate Kyber keypair for KEM."""
    try:
        public_key, secret_key = generate_keypair()
        session_data['public_key'] = public_key
        session_data['secret_key'] = secret_key
        
        return jsonify({
            'status': 'success',
            'message': 'Keys generated successfully',
            'public_key': bytes_to_b64(public_key),
            'public_key_size': len(public_key),
            'secret_key_size': len(secret_key),
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/encrypt', methods=['POST'])
def encrypt_text():
    """Encrypt plaintext using hybrid encryption."""
    try:
        data = request.json
        plaintext = data.get('plaintext', '')
        
        if not session_data['public_key']:
            return jsonify({'status': 'error', 'message': 'Generate keys first'}), 400
        
        if not plaintext:
            return jsonify({'status': 'error', 'message': 'Plaintext cannot be empty'}), 400
        
        # Step 1: Encapsulate shared secret using Kyber
        kem_ciphertext, shared_secret = encapsulate(session_data['public_key'])
        
        # Step 2: Use shared secret as AES key (truncate to 32 bytes)
        aes_key = shared_secret[:32]
        
        # Step 3: Encrypt plaintext with AES-256-GCM
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext, nonce, tag = encrypt_bytes(plaintext_bytes, aes_key)
        
        # Store for decryption
        session_data['last_ciphertext'] = {
            'kem_ciphertext': kem_ciphertext,
            'ciphertext': ciphertext,
            'nonce': nonce,
            'tag': tag,
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Encryption successful',
            'kem_ciphertext': bytes_to_b64(kem_ciphertext),
            'ciphertext': bytes_to_b64(ciphertext),
            'nonce': bytes_to_b64(nonce),
            'tag': bytes_to_b64(tag),
            'aes_key': bytes_to_b64(aes_key),
            'plaintext_size': len(plaintext_bytes),
            'ciphertext_size': len(ciphertext),
            'kem_ciphertext_size': len(kem_ciphertext),
            'shared_secret_size': len(shared_secret),
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/decrypt', methods=['POST'])
def decrypt_text():
    """Decrypt ciphertext using hybrid decryption."""
    try:
        data = request.json
        
        if not session_data['secret_key']:
            return jsonify({'status': 'error', 'message': 'Generate keys first'}), 400
        
        # Get ciphertext components from request
        kem_ciphertext = b64_to_bytes(data.get('kem_ciphertext', ''))
        ciphertext = b64_to_bytes(data.get('ciphertext', ''))
        nonce = b64_to_bytes(data.get('nonce', ''))
        tag = b64_to_bytes(data.get('tag', ''))
        
        # Step 1: Decapsulate shared secret using Kyber
        shared_secret = decapsulate(kem_ciphertext, session_data['secret_key'])
        
        # Step 2: Recovery AES key
        aes_key = shared_secret[:32]
        
        # Step 3: Decrypt with AES-256-GCM
        plaintext_bytes = decrypt_bytes(ciphertext, aes_key, nonce, tag)
        plaintext = plaintext_bytes.decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'message': 'Decryption successful',
            'plaintext': plaintext,
            'plaintext_size': len(plaintext_bytes),
            'aes_key': bytes_to_b64(aes_key),
            'shared_secret_size': len(shared_secret),
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/encrypt-file', methods=['POST'])
def encrypt_file_endpoint():
    """Encrypt uploaded file."""
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file provided'}), 400
        
        if not session_data['public_key']:
            return jsonify({'status': 'error', 'message': 'Generate keys first'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        # Read file content
        plaintext = file.read()
        filename = file.filename
        
        # Encrypt
        kem_ciphertext, shared_secret = encapsulate(session_data['public_key'])
        aes_key = shared_secret[:32]
        ciphertext, nonce, tag = encrypt_bytes(plaintext, aes_key)
        
        return jsonify({
            'status': 'success',
            'message': f'File encrypted: {filename}',
            'filename': filename,
            'original_size': len(plaintext),
            'ciphertext_size': len(ciphertext),
            'ciphertext': bytes_to_b64(ciphertext),
            'kem_ciphertext': bytes_to_b64(kem_ciphertext),
            'nonce': bytes_to_b64(nonce),
            'tag': bytes_to_b64(tag),
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
