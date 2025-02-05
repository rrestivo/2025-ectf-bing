# import json
# import struct
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend

# def load_secrets(secrets_file: str) -> bytes:
#     """Load AES key from the global secrets file."""
#     with open(secrets_file, "rb") as f:
#         secrets = json.loads(f.read())
#     return bytes.fromhex(secrets["some_secrets"])

# def decrypt_subscription(aes_key: bytes, encrypted_file: str):
#     """Decrypts the subscription file to verify encryption correctness."""
#     with open(encrypted_file, "rb") as f:
#         encrypted_data = f.read()

#     iv = encrypted_data[:16]  # Extract IV (first 16 bytes)
#     encrypted_subscription = encrypted_data[16:]  # Extract encrypted content

#     cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     decrypted_subscription = decryptor.update(encrypted_subscription) + decryptor.finalize()

#     # Unpack the decrypted subscription
#     decoder_id, start, end, channel = struct.unpack("<IQQI", decrypted_subscription)
#     print(f"\n✅ Decryption Successful! \n")
#     print(f"Decoder ID:   {hex(decoder_id)}")
#     print(f"Start Time:   {start}")
#     print(f"End Time:     {end}")
#     print(f"Channel ID:   {channel}")

# if __name__ == "__main__":
#     aes_key = load_secrets("secrets.json")
#     decrypt_subscription(aes_key, "subscription.enc")


import json
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from loguru import logger

# Constants for validation
CHANNEL_MIN = 0
CHANNEL_MAX = 8
DECODER_ID_MAX = 0xFFFFFFFF

def load_secrets(secrets_file: str) -> bytes:
    """Load AES key from the global secrets file."""
    try:
        with open(secrets_file, "rb") as f:
            secrets = json.loads(f.read())
    except FileNotFoundError:
        logger.error("Error: secrets.json file not found!")
        raise
    except json.JSONDecodeError:
        logger.error("Error: Invalid secrets.json format!")
        raise

    return bytes.fromhex(secrets["some_secrets"])

def decrypt_subscription(aes_key: bytes, encrypted_file: str):
    """Decrypts the subscription file to verify encryption correctness."""
    try:
        with open(encrypted_file, "rb") as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        logger.error("Error: subscription file not found!")
        raise

    # Extract IV (first 16 bytes) and encrypted content
    iv = encrypted_data[:16]
    encrypted_subscription = encrypted_data[16:]

    # Decrypt the subscription file using AES-128-CFB
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_subscription = decryptor.update(encrypted_subscription) + decryptor.finalize()

    # Unpack the decrypted subscription
    try:
        decoder_id, start, end, channel, nonce = struct.unpack("<IQQIQ", decrypted_subscription)
    except struct.error:
        logger.error("Decryption failed: Incorrect data format.")
        raise ValueError("Decryption failed: Data is not properly formatted!")

    # Validate the decoded fields
    if decoder_id < 0 or decoder_id > DECODER_ID_MAX:
        logger.error(f"Invalid Decoder ID: {hex(decoder_id)}. Must be a 4-byte unsigned integer.")
        raise ValueError("Invalid Decoder ID!")

    if start >= end:
        logger.error(f"Invalid time range: Start ({start}) >= End ({end}).")
        raise ValueError("Invalid time range! Start must be less than End.")

    if channel < CHANNEL_MIN or channel > CHANNEL_MAX:
        logger.error(f"Invalid Channel ID: {channel}. Must be between {CHANNEL_MIN} and {CHANNEL_MAX}.")
        raise ValueError("Invalid Channel ID!")

    # Output the successfully decrypted subscription details
    logger.success(f"\n✅ Decryption Successful!")
    logger.info(f"Decoder ID:   {hex(decoder_id)}")
    logger.info(f"Start Time:   {start}")
    logger.info(f"End Time:     {end}")
    logger.info(f"Channel ID:   {channel}")
    logger.info(f"Nonce:        {hex(nonce)} (Prevents Replay Attacks)")

if __name__ == "__main__":
    aes_key = load_secrets("secrets.json")
    decrypt_subscription(aes_key, "subscription.enc")
