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
import json
from pathlib import Path
import secrets

from loguru import logger


def gen_secrets(channels: list[int]) -> bytes:
    """Generate a secrets file with 10,008 channel keys and an extra secret_key.

    This function generates a JSON-encoded secrets file containing:
    1. A list of valid channels (provided as input).
    2. A dictionary of 10,008 channel keys, where each key is a 128-bit AES key.
    3. A master secret_key, which is also a 128-bit AES key.

    Args:
        channels (list[int]): A list of valid channel numbers. Channel 0 is reserved
            for emergency broadcasts and is always valid, so it is not included in
            this list.

    Returns:
        bytes: A JSON-encoded byte string containing the secrets.

  
    """
    secrets_dict = {
        "channels": channels,  # Retains original input for compatibility
        "channel_keys": {},
    }

    # Generate 10,008 keys with sequential channel IDs (1-10,007)
    
    for channel_id in range(1, 100):
        channel_key = secrets.token_bytes(16)  # Generate a 128-bit key
        secrets_dict["channel_keys"][channel_id] = channel_key.hex()  # Store as hex string

    # Generate the master secret_key
    secret_key = secrets.token_bytes(16)
    secrets_dict["secret_key"] = secret_key.hex()

    return json.dumps(secrets_dict).encode()


def generate_secrets_header(secrets_file: Path, header_file: Path):
    
    """Generate a C header file (`secrets.h`) from the secrets JSON file.

    This function reads the secrets JSON file, extracts the channel keys and secret_key,
    and writes them into a C-style header file. The header file contains:
    1. A 2D array `all_channel_keys` containing all 10,008 channel keys.
    2. A 1D array `secret_key` containing the master secret key.

    Args:
        secrets_file (Path): Path to the JSON file containing the secrets.
        header_file (Path): Path to the output C header file.

    Raises:
        Exception: If the secrets file is missing required keys or cannot be read.

   
    """
    try:
        # Read secrets JSON file
        with open(secrets_file, "r") as f:
            secrets = json.load(f)

        # Extract keys
        channel_keys = secrets.get("channel_keys", {})
        secret_key = secrets.get("secret_key", "")

        if not channel_keys or not secret_key:
            logger.error("Error: Missing required keys in secrets file.")
            return

        # Convert all channel keys to C-style array format
        all_keys_c = []
        for key in channel_keys.values():
            key_bytes = bytes.fromhex(key)
            key_hex = ", ".join(f"0x{b:02X}" for b in key_bytes)
            all_keys_c.append(f"{{ {key_hex} }}")

        # Convert secret_key to C-style array format
        secret_key_hex = ", ".join(f"0x{b:02X}" for b in bytes.fromhex(secret_key))

        # Ensure the output directory exists
        header_file.parent.mkdir(parents=True, exist_ok=True)

        # Write to `secrets.h`
        with open(header_file, "w") as f:
            f.write("#ifndef SECRETS_H\n")
            f.write("#define SECRETS_H\n\n")
            #f.write("#include <stdint.h>\n\n")

            # Write all channel keys as a single 2D array
            f.write("static const uint8_t all_channel_keys[100][16] = {\n")
            for row in all_keys_c:
                f.write(f"    {row},\n")
            f.write("};\n\n")

            # Write the secret_key as a 1D array
            f.write(f"static const uint8_t secret_key[16] = {{ {secret_key_hex} }};\n\n")

            f.write("#endif // SECRETS_H\n")

        logger.success(f"Generated {header_file}")

    except Exception as e:
        logger.error(f"Failed to generate secrets.h: {e}")


def parse_args():
    
    """Define and parse the command line arguments.

    This function sets up the command-line interface for the script. It accepts:
    1. A flag `--force` to overwrite an existing secrets file.
    2. A path to the secrets file to be created.
    3. A list of valid channel numbers.

    Returns:
        argparse.Namespace: Parsed command-line arguments.

 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force creation of secrets file, overwriting existing file",
    )
    parser.add_argument(
        "secrets_file",
        type=Path,
        help="Path to the secrets file to be created",
    )
    parser.add_argument(
        "channels",
        nargs="+",
        type=int,
        help="Supported channels. Channel 0 (broadcast) is always valid and will not"
        " be provided in this list",
    )
    return parser.parse_args()


def main():
    
    """Main function of the script.

    This function:
    1. Parses command-line arguments.
    2. Generates a secrets file using `gen_secrets`.
    3. Writes the secrets to the specified file.
    4. Generates a C header file (`secrets.h`) using `generate_secrets_header`.

    Example:
        To run the script:
        ```
        python gen_secrets.py --force secrets.json 1 2 3
        ```
    """
    # Parse the command line arguments
    args = parse_args()

    # Generate secrets
    secrets = gen_secrets(args.channels)

    # Write secrets to file
    with open(args.secrets_file, "wb" if args.force else "xb") as f:
        f.write(secrets)

    logger.success(f"Wrote secrets to {str(args.secrets_file.absolute())}")

    # Generate the `secrets.h` file in `decoder/inc/`
    #secrets_header_path = Path("./decoder/inc/secrets.h")
    secrets_header_path = Path("./global.secrets")
    generate_secrets_header(args.secrets_file, secrets_header_path)


if __name__ == "__main__":
    main()