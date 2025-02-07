**eCTF Encoder**


```python
import argparse
import struct
import json
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
```

- `argparse`: Handles command-line arguments.
- `struct`: Helps in binary data formatting.
- `json`: Parses JSON data (secrets file).
- `os`: Generates random values (IV for encryption).
- `cryptography.hazmat.primitives.ciphers`: Implements AES encryption.

---

## **2. AES S-Box Definition**
The AES S-Box (Substitution Box) is a predefined table used for byte substitution in encryption:

```python
AES_SBOX = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, ...] 
```

Each byte in the data is replaced using this S-box transformation to enhance security.

---

## **3. Encoder Class**
The `Encoder` class initializes the encryption system using a secret key from a JSON file.

### **3.1 Initialization**

```python
class Encoder:
    def __init__(self, secrets: bytes):
        secrets = json.loads(secrets)
        self.key = bytes.fromhex(secrets["some_secrets"])
        self.some_secrets = secrets["some_secrets"]
```

- `secrets` is a JSON file containing encryption keys.
- `self.key` extracts and stores a 128-bit AES key.
- `self.some_secrets` retains the original hex string for reference.

### **Example:**
**Input (JSON file `test.secrets`)**
```json
{"some_secrets": "2b7e151628aed2a6abf7158809cf4f3c"}
```
**Stored in `self.key`**:
```
b"+~\x15\x16(\xae\xd2\xa6\xab\xf7\x15\x88\t\xcfO<)"
```

---

## **4. AES Encryption Helper Function**

```python
def _aes_encrypt(self, data: bytes, key: bytes, iv: bytes, prepend_iv: bool = False) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    return (iv + ct) if prepend_iv else ct
```

- Encrypts data using **AES-128 in CFB mode**.
- Uses an **Initialization Vector (IV)** for randomness.
- If `prepend_iv=True`, IV is added to the ciphertext for decryption.

### **Example:**
**Input:**
```python
key = b"1234567890abcdef"
iv = b"0000000000000000"
data = b"Hello, world!"
```
**Output (Ciphertext):**
```
b'\xd4\xc1\x89\xfa...'
```

---

## **5. Applying AES S-Box Substitution**

```python
def _apply_sbox(self, data: bytes) -> bytes:
    return bytes(AES_SBOX[b] for b in data)
```

- Each byte in `data` is substituted using the AES S-Box table.

### **Example:**
**Input:** `b"AB" (ASCII: 65, 66)`
**Output:** `[AES_SBOX[65], AES_SBOX[66]] = b"\xa5\xe5"`

---

## **6. Encoding Function**

```python
def encode(self, channel: int, frame: bytes, timestamp: int) -> bytes:
```
### **6.1 Frame Preparation**
```python
if len(frame) > 64:
    raise ValueError("Frame size must not exceed 64 bytes.")
frame = frame.ljust(64, b'\x00')
```
- **Ensures frame size is at most 64 bytes**, padding with zeros if needed.

### **6.2 Inner Encryption (for non-channel 0)**
```python
if channel == 0:
    processed_frame = frame
else:
    fixed_iv = b'\x00' * 16
    inner_encrypted = self._aes_encrypt(frame, self.key, fixed_iv)
    processed_frame = self._apply_sbox(inner_encrypted)
```
- Encrypts frame with a **fixed IV** (all zeros) for consistency.
- Applies **AES S-box substitution**.

### **6.3 Adding Headers and Final Encryption**
```python
header = struct.pack("<IQ", channel, timestamp)
packet = header + processed_frame
random_iv = os.urandom(16)
final_encrypted = self._aes_encrypt(packet, self.key, random_iv, prepend_iv=True)
return final_encrypted
```
- **Header (12 bytes):**
  - `channel` (4 bytes, little-endian `I` format)
  - `timestamp` (8 bytes, little-endian `Q` format)
- **Outer AES-128-CFB encryption** with a **random IV** (16 bytes).

### **Example:**
**Input:**
```python
channel = 1
frame = b"Test Frame"
timestamp = 1678901234
```
**Output:**
```
b'\x8f\xe3\xaf\xbd... (92 encrypted bytes)'
```

---

## **7. Command-Line Interface (CLI)**
The script provides a command-line interface to test encoding:

```python
def main():
    parser = argparse.ArgumentParser(prog="ectf25_design.encoder")
    parser.add_argument("secrets_file", type=argparse.FileType("rb"), help="Path to the secrets file")
    parser.add_argument("channel", type=int, help="Channel to encode for")
    parser.add_argument("frame", help="Contents of the frame")
    parser.add_argument("timestamp", type=int, help="64b timestamp to use")
    args = parser.parse_args()
    encoder = Encoder(args.secrets_file.read())
    print(repr(encoder.encode(args.channel, args.frame.encode(), args.timestamp)))
```

### **Running the Script:**
```sh
python3 encoder.py test.secrets 1 "Hello" 100
```
**Output:**
```
b'\xa5\x87\xd1\xf9...'  # Encrypted frame
```


##  -----------------------------------------  ** Explanation for Adav_Enocder  logic ** -------------------------------------------




It securely encrypts messages using **AES-128 in CFB mode**, implementing **key rotation and hierarchical key derivation**.

## 🔹 How It Works
1. **Key Derivation**  
   - A **unique key is derived per channel** and **rotated every 5 minutes**.
   - **Outer Key** is derived from the **Master Key** using **Channel ID + Time Bucket**.
   - **Inner Key** is derived **from the Outer Key** for additional security.

2. **Two-Layer Encryption**
   - The **Inner Key encrypts** the raw frame first.
   - The **Outer Key encrypts** (Channel ID + Timestamp + Inner Encrypted Frame).
   - Ensures metadata is protected while allowing authentication.

   

## ------------------------------------------------------------------------------------------------------------------------------------------

# How the Decoder Works with the Encoder

| Step | Encoder | Decoder |
|------|---------|---------|
| **1** | Derives **Outer Key** from (Master Key + Channel ID + Time Bucket) | Derives the same **Outer Key** (checking `T`, `T-1`, `T+1`) |
| **2** | Encrypts **(Channel ID + Timestamp + Inner Encrypted Frame)** using **Outer Key** | Decrypts the **Outer Layer** using the same **Outer Key** |
| **3** | Extracts the **Channel ID and Timestamp** | Extracts and validates the **Channel ID and Timestamp** |
| **4** | Derives **Inner Key** from **Outer Key** | Derives **Inner Key** from the same **Outer Key** |
| **5** | Encrypts the **Raw Frame** using the **Inner Key** | Decrypts the **Inner Layer** using the **Inner Key** |
| **6** | Sends encrypted data | Recovers the **original message** |

---

### **Now the Decoder:**
- **Handles clock drift** by trying multiple time buckets.
-  **Follows the same key derivation logic** as the encoder.
-  **Decrypts in two stages (Outer Layer → Inner Layer).**
-  **Logs decryption steps for debugging.**





### ------------------------- output for advanced -------------------------------

raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design$ python3 Adv_enoder.py  my_secrets.json 3 "hello" 3
2025-02-07 14:52:42.929 | INFO     | __main__:<module>:28 - Encoder started...
2025-02-07 14:52:42.953 | INFO     | __main__:__init__:47 - Encoder initialized with allowed channels: [0, 1, 2, 3, 4, 5, 6, 7, 8]
2025-02-07 14:52:42.966 | INFO     | __main__:encode:114 - Encoding started for Channel 3 at Timestamp 3
2025-02-07 14:52:43.071 | INFO     | __main__:_derive_outer_key:73 - Derived outer key for Channel 3 | Time Bucket 14491316: a678e49e76557fdf250d420c99dd7368
2025-02-07 14:52:43.072 | INFO     | __main__:_derive_inner_key:91 - Derived inner key from outer key: d249e2d47ea1b9ff78f085b5c18bfaf3
2025-02-07 14:52:43.076 | INFO     | __main__:_aes_encrypt:105 - Data encrypted with AES-128 CFB.
2025-02-07 14:52:43.076 | INFO     | __main__:encode:128 - Inner encryption complete for channel 3.
2025-02-07 14:52:43.077 | INFO     | __main__:_aes_encrypt:105 - Data encrypted with AES-128 CFB.
2025-02-07 14:52:43.077 | INFO     | __main__:encode:136 - Full packet encrypted for Channel 3 | Timestamp: 3 | Encrypted Data: 000000000000000000000000000000004a57f1c6cf60315ce94453adbb660e2ae85bb9643d96383596a4e3528f062dfc49dcddae99047498456d2e9bd69f26c4438c3762637baaebaa3c19c48c293b22538769633c52088dced8d495
Encoded Data: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00JW\xf1\xc6\xcf`1\\\xe9DS\xad\xbbf\x0e*\xe8[\xb9d=\x9685\x96\xa4\xe3R\x8f\x06-\xfcI\xdc\xdd\xae\x99\x04t\x98Em.\x9b\xd6\x9f&\xc4C\x8c7bc{\xaa\xeb\xaa<\x19\xc4\x8c);"S\x87ic<R\x08\x8d\xce\xd8\xd4\x95'
raj@Vivek:/mnt/c/Users/rajvi/OneDrive/Desktop/2025_ECTF/2025-ectf-bing/design/ectf25_design$ python3 Adv_enoder.py  my_secrets.json 100 "hello" 3
2025-02-07 14:53:56.557 | INFO     | __main__:<module>:28 - Encoder started...
2025-02-07 14:53:56.560 | INFO     | __main__:__init__:47 - Encoder initialized with allowed channels: [0, 1, 2, 3, 4, 5, 6, 7, 8]
2025-02-07 14:53:56.560 | INFO     | __main__:encode:114 - Encoding started for Channel 100 at Timestamp 3
2025-02-07 14:53:56.561 | ERROR    | __main__:_derive_outer_key:58 - Unauthorized channel 100 attempted!
