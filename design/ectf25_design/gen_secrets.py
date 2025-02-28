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
import secrets
from pathlib import Path
from loguru import logger


def gen_secrets(channels: list[int]) -> str:
    """Generate secrets in C header format instead of JSON.

    Args:
        channels (list[int]): List of valid channel numbers.

    Returns:
        str: C header content containing all channel keys and a master secret key.
    """
    all_keys_c = []
    
    # Generate 100 keys (Modify to 10,008 if needed)
    for channel_id in range(1, 100):  # Change 100 to 10008 for full keyset
        channel_key = secrets.token_bytes(16)  # Generate a 128-bit AES key
        key_hex = ", ".join(f"0x{b:02X}" for b in channel_key)
        all_keys_c.append(f"    {{ {key_hex} }}")

    # Generate master secret key
    secret_key = secrets.token_bytes(16)
    secret_key_hex = ", ".join(f"0x{b:02X}" for b in secret_key)

    # Format as C header content
    header_content = """#ifndef SECRETS_H
#define SECRETS_H

#include <stdint.h>

static const uint8_t all_channel_keys[100][16] = {
"""
    header_content += ",\n".join(all_keys_c) + "\n};\n\n"

    header_content += f"static const uint8_t secret_key[16] = {{ {secret_key_hex} }};\n\n"
    header_content += "#endif // SECRETS_H\n"

    return header_content


def save_secrets_file(file_path: Path, content: str):
    """Save the generated secrets as a C header file.

    Args:
        file_path (Path): Path to save the file.
        content (str): C header content to write.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)
    logger.success(f"Generated {file_path}")


def parse_args():
    """Parse the command-line arguments."""
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
    """Main function to generate secrets in C header format."""
    args = parse_args()

    # Generate secrets in C header format
    secrets_content = gen_secrets(args.channels)

    # Save to `secrets.h`
    secrets_h_path = Path("./decoder/inc/secrets.h")
    save_secrets_file(secrets_h_path, secrets_content)

    # Save to `global.secrets` (Same C format as `secrets.h`)
    global_secrets_path = Path("./global.secrets")
    save_secrets_file(global_secrets_path, secrets_content)


if __name__ == "__main__":
    main()
