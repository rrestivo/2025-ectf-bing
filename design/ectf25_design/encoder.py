"""
Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import argparse
import struct
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from loguru import logger


class Encoder:
    def __init__(self, secrets: bytes):
        """Initialize with channel-specific keys and secret_key"""
        secrets = json.loads(secrets)
        self.channel_keys = {int(c): bytes.fromhex(k) for c, k in secrets["channel_keys"].items()}
        self.secret_key = bytes.fromhex(secrets["secret_key"])

        logger.info("Successfully loaded channel keys and secret_key.")
        logger.debug(f"Available channel keys: {list(self.channel_keys.keys())}")
        logger.debug(f"Final encryption key (secret_key): {self.secret_key.hex()}")
        
        

    def _encrypt(self, data: bytes, key: bytes) -> bytes:
        """Encrypt data using AES-ECB mode"""
        logger.debug(f"Encrypting data with key: {key.hex()}")
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return encrypted_data
    
    
    

    # def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
    #     """Encode a frame"""

    #     logger.info(f"Encoding frame for Channel = {channel}, Timestamp = {timestamp}")

    #     if len(frame) > 64:
    #         raise ValueError("Frame size must not exceed 64 bytes.")

    #     logger.debug(f"Frame length before padding: {len(frame)} bytes")

    #     # --------------- Step 1: Calculate padding for frame to nearest multiple of 16
    #     frame_size = len(frame)
    #     if frame_size % 16 != 0:
    #         frame_padding = 16 - (frame_size % 16)
    #         frame += b'\x00' * frame_padding

    #     # Step 3: Choose encryption key
    #     if channel == 0:
    #         # Using  secret_key for channel 0 in both encryptions
    #         channel_key = self.secret_key  
    #     else:
    #         if channel not in self.channel_keys:
    #             raise ValueError(f"No key found for channel {channel}. Available channels: {list(self.channel_keys.keys())}")
    #         channel_key = self.channel_keys[channel]

    #     logger.info(f"Using encryption key for channel {channel}: {channel_key.hex()}")

    #     #------- Step 4: First encryption layer on (padded frame)
    #     encrypted_frame = self._encrypt(frame, channel_key)
    #     logger.success(f"First encryption complete for channel {channel}. Encrypted Frame Size: {len(encrypted_frame)} bytes")

    #     # ---------- Step 5: Pack header (channel_id + timestamp + padd_done)
    #     header = struct.pack("<IQI", channel, timestamp, frame_size)
    #     logger.debug(f"Packed Header Structure (Hex): {header.hex()} (Channel = {channel}, Timestamp = {timestamp}, frame size = {frame_size})")

    #     #---------- Step 6: Create full packet
    #     full_packet = header + encrypted_frame
    #     logger.debug(f"Full Packet Length Before Final Padding: {len(full_packet)} bytes")

    #     #------------ Step 7:  padding to make the full packet a multiple of 16
    #     if len(full_packet) %16 != 0:
    #         padding_length = 16 - (len(full_packet) %16) 
    #         full_packet += b'\x00' * padding_length

    #     logger.info(f"Final Packet Size After Padding: {len(full_packet)} bytes (Multiple of 16)")
    #     logger.debug(f"Final Packet Before Second Encryption (Hex): {full_packet.hex()}")

    #     # Step 8: Second encryption on (header + encrypted_frame)
    #     encrypted_packet = self._encrypt(full_packet, self.secret_key)
    #     logger.success(f"Final encryption complete using secret_key. Final Encrypted Packet Size: {len(encrypted_packet)} bytes")
    #     logger.debug(f"Final Encrypted Packet Structure (Hex): {encrypted_packet.hex()}")

    #     return encrypted_packet
    def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
        """Encode a frame"""
        logger.info(f"Encoding frame for Channel = {channel}, Timestamp = {timestamp}")

        if len(frame) > 64:
            raise ValueError("Frame size must not exceed 64 bytes.")

        logger.debug(f"Frame length before padding: {len(frame)} bytes")

        # Calculate effective channel ID using modulo 10007
        effective_channel = channel % 10007
        logger.debug(f"Effective channel ID after modulo: {effective_channel}")

        # --------------- Step 1: Calculate padding for frame to nearest multiple of 16
        frame_size = len(frame)
        if frame_size % 16 != 0:
            frame_padding = 16 - (frame_size % 16)
            frame += b'\x00' * frame_padding

        # Step 3: Choose encryption key based on effective channel ID
        if effective_channel == 0:
            # Using secret_key for channel 0 in both encryptions
            channel_key = self.secret_key  
        else:
            if effective_channel not in self.channel_keys:
                raise ValueError(f"No key found for effective channel {effective_channel}. Available channels: {list(self.channel_keys.keys())}")
            channel_key = self.channel_keys[effective_channel]

        logger.info(f"Using encryption key for effective channel {effective_channel}: {channel_key.hex()}")

        #------- Step 4: First encryption layer on (padded frame)
        encrypted_frame = self._encrypt(frame, channel_key)
        logger.success(f"First encryption complete for channel {channel}. Encrypted Frame Size: {len(encrypted_frame)} bytes")

        # ---------- Step 5: Pack header (channel_id + timestamp + padd_done)
        header = struct.pack("<IQI", channel, timestamp, frame_size)
        logger.debug(f"Packed Header Structure (Hex): {header.hex()} (Channel = {channel}, Timestamp = {timestamp}, frame size = {frame_size})")

        #---------- Step 6: Create full packet
        full_packet = header + encrypted_frame
        logger.debug(f"Full Packet Length Before Final Padding: {len(full_packet)} bytes")

        #------------ Step 7:  padding to make the full packet a multiple of 16
        if len(full_packet) %16 != 0:
            padding_length = 16 - (len(full_packet) %16) 
            full_packet += b'\x00' * padding_length

        logger.info(f"Final Packet Size After Padding: {len(full_packet)} bytes (Multiple of 16)")
        logger.debug(f"Final Packet Before Second Encryption (Hex): {full_packet.hex()}")

        # Step 8: Second encryption on (header + encrypted_frame)
        encrypted_packet = self._encrypt(full_packet, self.secret_key)
        logger.success(f"Final encryption complete using secret_key. Final Encrypted Packet Size: {len(encrypted_packet)} bytes")
        logger.debug(f"Final Encrypted Packet Structure (Hex): {encrypted_packet.hex()}")

        return encrypted_packet



def main():
    """Main function to encode a frame"""
    parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
    parser.add_argument("secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file")
    parser.add_argument("channel", type=int, help="Channel to encode for")
    parser.add_argument("frame", help="Contents of the frame")
    parser.add_argument("timestamp", type=int, help="64b timestamp to use")
    args = parser.parse_args()

    encoder = Encoder(args.secrets_file.read())
    print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))


if __name__ == "__main__":
    main()
