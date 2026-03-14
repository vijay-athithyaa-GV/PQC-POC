import time
import os
import csv

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from quantumshield.core.aes_module import (
    generate_aes_key,
    encrypt_bytes,
    decrypt_bytes
)

runs = 100
data = os.urandom(32)

# AES setup
aes_key = generate_aes_key()

aes_enc_total = 0
aes_dec_total = 0

for _ in range(runs):
    start = time.time()
    ciphertext, nonce, tag = encrypt_bytes(data, aes_key)
    aes_enc_total += time.time() - start

    start = time.time()
    decrypt_bytes(ciphertext, aes_key, nonce, tag)
    aes_dec_total += time.time() - start

aes_enc = aes_enc_total / runs
aes_dec = aes_dec_total / runs


# RSA setup
rsa_key = RSA.generate(2048)
cipher_enc = PKCS1_OAEP.new(rsa_key.publickey())
cipher_dec = PKCS1_OAEP.new(rsa_key)

rsa_enc_total = 0
rsa_dec_total = 0

for _ in range(runs):
    start = time.time()
    rsa_cipher = cipher_enc.encrypt(data)
    rsa_enc_total += time.time() - start

    start = time.time()
    cipher_dec.decrypt(rsa_cipher)
    rsa_dec_total += time.time() - start

rsa_enc = rsa_enc_total / runs
rsa_dec = rsa_dec_total / runs


print("\nCrypto Benchmark Results")
print(f"AES Encrypt Avg: {aes_enc:.6f} sec")
print(f"AES Decrypt Avg: {aes_dec:.6f} sec")
print(f"RSA Encrypt Avg: {rsa_enc:.6f} sec")
print(f"RSA Decrypt Avg: {rsa_dec:.6f} sec")


# Save results to CSV
with open("benchmark_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Algorithm", "Encrypt Time", "Decrypt Time"])
    writer.writerow(["AES", aes_enc, aes_dec])
    writer.writerow(["RSA", rsa_enc, rsa_dec])

print("\nResults saved to benchmark_results.csv")