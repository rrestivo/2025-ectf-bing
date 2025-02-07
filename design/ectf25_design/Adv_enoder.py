"""
Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF (eCTF).
This code is being provided only for educational purposes for the 2025 MITRE eCTF competition.
Use this code at your own risk!

Copyright: (c) 2025 The MITRE Corporation
"""

import argparse
import struct
import json
import os
import hmac
import hashlib
from sbox import AES_SBOX
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from loguru import logger  # Added logging module

# Configure logger
logger.add("encoder.log", format="{time} {level} {message}", level="INFO")

class Encoder:
    def __init__(self, secrets: bytes):
        """
        Initializes the encoder using the global secrets.

        :param secrets: JSON content of the secrets file.
        """
        # Parse the JSON secrets file.
        secrets = json.loads(secrets)

        # Master key used for key rotation (128-bit AES key from secrets file)
        self.master_key = bytes.fromhex(secrets["some_secrets"])

        # Allowed channels from the secrets file
        self.allowed_channels = secrets["channels"]

        logger.info("Encoder initialized with allowed channels: {}", self.allowed_channels)
        
        

    def _derive_session_key(self, channel: int) -> bytes:
        if channel not in self.allowed_channels:
            logger.error("Unauthorized channel {} attempted!", channel)
            raise ValueError(f"Unauthorized channel {channel}. Not in allowed list.")

    
        salt = hmac.new(self.master_key, struct.pack("<H", channel), digestmod=hashlib.sha256).digest()

        # Generate session key using HKDF
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=16,  # AES-128 key size
            salt=salt,
            info=b"eCTF-channel-key-rotation",
        )
        session_key = hkdf.derive(self.master_key)

        logger.info("Derived session key for Channel {}: {}", channel, session_key.hex())
        return session_key
    
    
    




    def _aes_encrypt(self, data: bytes, key: bytes, iv: bytes, prepend_iv: bool = False) -> bytes:
        """
        Encrypts data using AES-128 in CFB mode.

        :param data: Data to encrypt.
        :param key: Encryption key.
        :param iv: Initialization vector.
        :param prepend_iv: If True, the IV is prepended to the ciphertext.
        :return: Encrypted data.
        """
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(data) + encryptor.finalize()
        return (iv + ct) if prepend_iv else ct

    def _apply_sbox(self, data: bytes) -> bytes:
        """Apply the AES S-box substitution to each byte of the data."""
        return bytes(AES_SBOX[b] for b in data)

    def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
        """
        Encrypts a frame for transmission.

        :param channel: Channel number.
        :param frame: Frame data (max 64 bytes).
        :param timestamp: Timestamp.
        :return: Encrypted frame.
        """
        logger.info("Encoding started for Channel {} at Timestamp {}", channel, timestamp)

        if len(frame) > 64:
            logger.error("Frame size exceeded limit: {} bytes", len(frame))
            raise ValueError("Frame size must not exceed 64 bytes.")

        frame = frame.ljust(64, b'\x00')  # Pad frame to 64 bytes
        session_key = self._derive_session_key(channel)

        if channel == 0:
            processed_frame = frame
        else:
            fixed_iv = b'\x00' * 16
            inner_encrypted = self._aes_encrypt(frame, session_key, fixed_iv, prepend_iv=False)
            processed_frame = self._apply_sbox(inner_encrypted)

        header = struct.pack("<IQ", channel, timestamp)
        packet = header + processed_frame

        random_iv = b'\x00' * 16
        final_encrypted = self._aes_encrypt(packet, session_key, random_iv, prepend_iv=True)

        logger.info("Encoded frame for Channel {} | Timestamp: {} | Encrypted Data: {}", 
                    channel, timestamp, final_encrypted.hex())

        return final_encrypted


def main():
    """A test main to one-shot encode a frame"""
    parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
    parser.add_argument("secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file")
    parser.add_argument("channel", type=int, help="Channel to encode for")
    parser.add_argument("frame", help="Contents of the frame")
    parser.add_argument("timestamp", type=int, help="64-bit timestamp to use")
    args = parser.parse_args()

    encoder = Encoder(args.secrets_file.read())
    encrypted_data = encoder.encode(args.channel, args.frame.encode(), args.timestamp)

    print("Encoded Data:", repr(encrypted_data))


if __name__ == "__main__":
    main()
