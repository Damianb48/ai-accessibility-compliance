"""Utilities for encrypting and decrypting secrets.

This module provides thin wrappers around the `cryptography` library to
perform AES‑256‑GCM encryption and decryption. Keys should be rotated
regularly; you can store an encrypted version of your Supabase service
role key or Stripe webhook secret on disk and decrypt it at runtime.
"""

import base64
import os
from typing import Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_key() -> str:
    """Generate a new 256‑bit key and return it as a base64 string."""
    key = AESGCM.generate_key(bit_length=256)
    return base64.b64encode(key).decode()


def encrypt(key_b64: str, plaintext: str) -> Tuple[str, str]:
    """Encrypt a plaintext string using AES‑256‑GCM.

    Args:
        key_b64: Base64‑encoded 256‑bit key.
        plaintext: The value to encrypt.

    Returns:
        A tuple of (nonce_b64, ciphertext_b64) where the ciphertext
        includes the authentication tag.
    """
    key = base64.b64decode(key_b64)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96‑bit nonce recommended for GCM
    ct = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce).decode(), base64.b64encode(ct).decode()


def decrypt(key_b64: str, nonce_b64: str, ciphertext_b64: str) -> str:
    """Decrypt a ciphertext encrypted with :func:`encrypt`.

    Args:
        key_b64: The same base64 key used for encryption.
        nonce_b64: Base64‑encoded nonce returned by `encrypt`.
        ciphertext_b64: Base64‑encoded ciphertext returned by `encrypt`.

    Returns:
        The original plaintext string.
    """
    key = base64.b64decode(key_b64)
    nonce = base64.b64decode(nonce_b64)
    ct = base64.b64decode(ciphertext_b64)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ct, None)
    return plaintext.decode()
