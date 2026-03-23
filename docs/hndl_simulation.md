# HNDL Threat Simulation (Logic Only)

## Scenario
An attacker records encrypted data today and stores it for future decryption once a large-scale quantum computer exists.

## Case 1: RSA-encrypted AES key
- Today: A file is encrypted with AES, and the AES key is wrapped with RSA.
- Future: A sufficiently large quantum computer can use Shor's algorithm to break RSA and recover the AES key.
- Outcome: The stored ciphertext becomes readable once the RSA key is broken.

## Case 2: Kyber-encrypted AES key
- Today: A file is encrypted with AES, and the AES key is derived from a Kyber KEM shared secret.
- Future: Current understanding suggests Kyber remains resistant to known quantum attacks.
- Outcome: The stored ciphertext remains protected even with quantum capabilities.

## Summary
This simulation illustrates why post-quantum KEMs like Kyber are used in hybrid designs to mitigate harvest-now, decrypt-later risks.
