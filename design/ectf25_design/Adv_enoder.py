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
import time
from sbox import AES_SBOX
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from loguru import logger  # Logging module

# Configure logger
logger.add("encoder.log", format="{time} {level} {message}", level="INFO")
logger.info("Encoder started...")



class Encoder:
    def __init__(self, secrets: bytes):
        """
        Initializes the encoder using the global secrets.

      
        """
        
        secrets = json.loads(secrets)

        # Master key used for key rotation (128-bit AES key from secrets file)
        self.master_key = bytes.fromhex(secrets["some_secrets"])

        # Allowed channels from the secrets file
        self.allowed_channels = secrets["channels"]
        logger.info("Encoder initialized with allowed channels: {}", self.allowed_channels)
        
        

    def _derive_outer_key(self, channel: int, time_offset: int = 0) -> bytes:
        """
        Derives the first-level (outer encryption) key using the master key.
        This key is based on channel ID and a time-based rotation mechanism.

        """
        if channel not in self.allowed_channels:
            logger.error("Unauthorized channel {} attempted!", channel)
            raise ValueError(f"Unauthorized channel {channel}. Not in allowed list.")

        rotation_interval = 120  # 120 seconds
        time_bucket = (int(time.time()) // rotation_interval) + time_offset 

        salt = hmac.new(self.master_key, struct.pack("<HI", channel, time_bucket), digestmod=hashlib.sha256).digest()

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=16,
            salt=salt,
            info=b"eCTF-outer-layer",
        )
        outer_key = hkdf.derive(self.master_key)
        logger.info("Derived outer key for Channel {} | Time Bucket {}: {}", channel, time_bucket, outer_key.hex())
        return outer_key




    def _derive_inner_key(self, outer_key: bytes) -> bytes:
        """
        Derives the second-level (inner encryption) key from the outer encryption key.
        """
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=16,
            salt=b"inner-layer-salt",
            info=b"eCTF-inner-layer",
        )
        inner_key = hkdf.derive(outer_key)

        logger.info("Derived inner key from outer key: {}", inner_key.hex())

        return inner_key
    
    
    

    def _aes_encrypt(self, data: bytes, key: bytes, iv: bytes, prepend_iv: bool = False) -> bytes:
        """
        Encrypts data using AES-128 in CFB mode.
        """
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(data) + encryptor.finalize()
        logger.info("Data encrypted with AES-128 CFB.")
        return (iv + ct) if prepend_iv else ct



    def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
        """
        Encrypts a frame using two-layer encryption with hierarchical key derivation.
        """
        logger.info("Encoding started for Channel {} at Timestamp {}", channel, timestamp)

        if len(frame) > 64:
            logger.error("Frame size exceeded limit: {} bytes", len(frame))
            raise ValueError("Frame size must not exceed 64 bytes.")

        frame = frame.ljust(64, b'\x00')

        outer_key = self._derive_outer_key(channel)
        inner_key = self._derive_inner_key(outer_key)

        fixed_iv = b'\x00' * 16
        encrypted_frame = self._aes_encrypt(frame, inner_key, fixed_iv, prepend_iv=False)

        logger.info("Inner encryption complete for channel {}.", channel)

        header = struct.pack("<IQ", channel, timestamp)
        packet = header + encrypted_frame

        random_iv = b'\x00' * 16
        fully_encrypted_packet = self._aes_encrypt(packet, outer_key, random_iv, prepend_iv=True)

        logger.info("Full packet encrypted for Channel {} | Timestamp: {} | Encrypted Data: {}", 
                    channel, timestamp, fully_encrypted_packet.hex())

        return fully_encrypted_packet






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
