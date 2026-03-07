"""Binary package format for QuantumShield encrypted files."""

from __future__ import annotations

MAGIC_HEADER = b"QSHIELD"
VERSION = 1
KYBER_LEN_SIZE_BYTES = 4
NONCE_SIZE_BYTES = 12
TAG_SIZE_BYTES = 16


def build_package(kyber_ct: bytes, nonce: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    """Build a binary package containing all hybrid encryption components."""

    if not isinstance(kyber_ct, (bytes, bytearray)):
        raise TypeError("kyber_ct must be bytes")
    if not isinstance(nonce, (bytes, bytearray)):
        raise TypeError("nonce must be bytes")
    if not isinstance(tag, (bytes, bytearray)):
        raise TypeError("tag must be bytes")
    if not isinstance(ciphertext, (bytes, bytearray)):
        raise TypeError("ciphertext must be bytes")
    if len(nonce) != NONCE_SIZE_BYTES:
        raise ValueError("nonce must be 12 bytes")
    if len(tag) != TAG_SIZE_BYTES:
        raise ValueError("tag must be 16 bytes")

    kyber_len = len(kyber_ct).to_bytes(KYBER_LEN_SIZE_BYTES, "big")
    return b"".join(
        [
            MAGIC_HEADER,
            bytes([VERSION]),
            kyber_len,
            bytes(kyber_ct),
            bytes(nonce),
            bytes(tag),
            bytes(ciphertext),
        ]
    )


def parse_package(data: bytes) -> tuple[bytes, bytes, bytes, bytes]:
    """Parse a binary package and return its components.

    Returns:
        (kyber_ct, nonce, tag, ciphertext)
    """

    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")

    min_size = len(MAGIC_HEADER) + 1 + KYBER_LEN_SIZE_BYTES + NONCE_SIZE_BYTES + TAG_SIZE_BYTES
    if len(data) < min_size:
        raise ValueError("package is too short")

    offset = 0
    magic = data[offset : offset + len(MAGIC_HEADER)]
    if magic != MAGIC_HEADER:
        raise ValueError("invalid magic header")
    offset += len(MAGIC_HEADER)

    version = data[offset]
    if version != VERSION:
        raise ValueError("unsupported package version")
    offset += 1

    kyber_len = int.from_bytes(data[offset : offset + KYBER_LEN_SIZE_BYTES], "big")
    offset += KYBER_LEN_SIZE_BYTES

    kyber_end = offset + kyber_len
    if kyber_end + NONCE_SIZE_BYTES + TAG_SIZE_BYTES > len(data):
        raise ValueError("invalid Kyber ciphertext length")

    kyber_ct = bytes(data[offset:kyber_end])
    offset = kyber_end

    nonce = bytes(data[offset : offset + NONCE_SIZE_BYTES])
    offset += NONCE_SIZE_BYTES

    tag = bytes(data[offset : offset + TAG_SIZE_BYTES])
    offset += TAG_SIZE_BYTES

    ciphertext = bytes(data[offset:])

    return kyber_ct, nonce, tag, ciphertext
