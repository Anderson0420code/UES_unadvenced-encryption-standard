# UES_unadvenced-encryption-standard
A system for anti ai crawling If bugs/problems found, please contact andersonlilife@icloud.com or make a branch
 # unadvanced-encryption-standard (UES) Technical & Web GUI Documentation

`unadvanced-encryption-standard` is a data steganography and camouflage protection system implemented via Python and modern browser-native JavaScript (Web GUI). The primary design goal of this system is **anti-AI web crawling and unauthorized data harvesting**. By employing data compression, Pseudo-Random Number Generator (PRNG) permutations, matrix transformations, and character/image encoding, raw text, confidential files, or images are transformed into text or grayscale noise images that AI crawlers cannot parse or extract semantic features from, preventing data from being ingested into AI model training sets.

---

## System Design Goals & Principles

Traditional text and images on the public web are easily analyzed by automated crawlers and utilized to train Large Language Models (LLMs) or vision models. This system disrupts this process through the following mechanisms:

1. **Semantic Structure Destruction**: Compresses text, subjects it to dual/dynamic chaotic permutations, and maps it to semantically unrelated Unicode Chinese character blocks (`0x4E00` offset), ensuring text crawlers only extract meaningless character combinations.
2. **Image Data Noisification**: Extracts raw RGBA image pixel data, compresses and permutes it, and repackages it into single-channel grayscale (Mode 'L') or pixel noise images, blinding image crawlers to original visual features.
3. **Dynamic Boundary Noise**: Wraps outer pseudo-random generated walls around the core data matrix to interfere with automated feature extraction algorithms.
4. **Zero-Backend Pure Frontend (Web GUI)**: Provides a serverless web workbench based on HTML5 Canvas, Tailwind CSS, and JavaScript (Pako Zlib, Web Crypto API), ensuring total local privacy protection inside the browser.

---

## Module Architecture

The system comprises three core modules, each featuring a Python backend engine and an independent pure-frontend Web GUI tool.

```
UES System Architecture
│
├── 1. D-Series (Text & Document Protection)
│   ├── UES-D01: Fixed 66x66 Matrix (For short text/passwords) [Python & HTML GUI]
│   └── UES-D02: Adaptive Dynamic N×N Matrix + Precise M=N+2 Wall (For arbitrary length text) [Python & HTML GUI]
│
└── 2. P-Series (Image Data Protection)
    └── UES-P01: RGBA Pixel Compression/Obfuscation + Grayscale Noise Wall Image [Python & HTML GUI]
```

---

### 1. D-Series: Text & Document Protection Modules

#### UES-D01 (Fixed-Size Text Cipher - 66×66 Matrix)
* **Applicable Scenarios**: Short texts, passwords, or fixed-length data protection.
* **Technical Details**:
  * **Key Processing**: Processes input key into 32 bytes (256-bit) and derives PRNG seed via `SHA-256`.
  * **Capacity Limit**: Raw text length $L$ after `zlib` (Level 9) compression must not exceed 63 bytes.
  * **Matrix Transformation**:
    1. Perform 1D key permutation on 64 bytes.
    2. Expand into a $64 \times 64$ core matrix via circular shift (`np.roll`).
    3. Wrap 1 layer of pseudo-random noise walls around the core matrix to construct a $66 \times 66$ matrix (4,356 elements total).
    4. Perform global secondary shuffling on the $66 \times 66$ array.
  * **Output Encoding**: Mapped to Unicode common Chinese character section (`0x4E00`), outputting exactly 4,356 Chinese characters.
* **GUI Tool**: `UES-D01.html` (Featuring 66×66 Canvas heatmap rendering, data probes, and avalanche testing).

#### UES-D02 (Dynamic-Size Text Cipher - Adaptive Matrix)
* **Applicable Scenarios**: Arbitrary-length text or document content protection.
* **Technical Details**:
  * **Key Processing**: Uses `SHA-256` to derive three independent 32-bit integer seeds (`prng_core`, `prng_pad`, `prng_wall`).
  * **Dynamic Dimension Calculation**:
    Let $L$ be the byte length of text after `zlib` compression. The minimum core square matrix side length $N$ is calculated as:
    $$N = \lceil \sqrt{L + 1} \rceil$$
  * **Wall Structure**: Adds 1 layer of noise wall around the $N \times N$ core, forming a matrix of side length $M = N + 2$ (total elements $M^2$).
  * **Output Encoding**: Dynamically generates a Unicode Chinese string of length $M^2$ (`0x4E00` offset).
* **GUI Tool**: `UES-D02.html` (Supports dynamic N×N / M×M visualization and 5-step pipeline dissection).

---

### 2. P-Series: Image Protection Module

#### UES-P01 (Image Data Steganography Protection)
* **Applicable Scenarios**: Anti-AI crawler protection for PNG, JPEG, and other image formats.
* **Technical Details**:
  * **Data Extraction & Header Construction**: Reads raw RGBA pixel data of the image, establishing an 8-byte Header containing 32-bit width and height.
  * **Data Compression & Obfuscation**: Compresses payload using `zlib` (Level 9), applying bitwise XOR and position permutation on pixel arrays via MT19937 PRNG.
  * **Wall Encapsulation & Image Output**: Wraps defensive noise around the perimeter, exporting the array into a grayscale noise map or pixel-obfuscated image resistant to AI feature extraction.
* **GUI Tool**: `UES-P01.html` (Provides single-page drag-and-drop upload, real-time preview, and local restoration).

---

## Frontend GUI Interface Usage

The project provides three serverless Single Page Applications (SPAs):

1. **`UES-D01.html`**: Open directly in a browser to perform encryption, decryption, and heatmap probe analysis on a fixed 66×66 matrix.
2. **`UES-D02.html`**: Supports long-text adaptive dynamic matrix encryption, featuring visual Canvas matrix scaling and key avalanche testing.
3. **`UES-P01.html`**: Provides browser-native anti-crawler image encryption and reverse decryption, ensuring images are never transmitted to third-party servers.

---

## Python Script Usage Examples

### 1. UES-D02 Dynamic Text Encryption & Decryption

```python
from UES_D02 import ues_dynamic_encrypt, ues_dynamic_decrypt

key = "secret-key-2026"
text = "這是一段需要防止被 AI 爬蟲抓取的機密文件內容。"

# Encryption
result = ues_dynamic_encrypt(text, key)
disguised_text = result["disguised_text"]
print("Encrypted Result (Unicode Chinese String):", disguised_text)

# Decryption
restored_text = ues_dynamic_decrypt(disguised_text, key)
print("Decrypted Result:", restored_text)
```

### 2. UES-P01 Image Protection & Restoration

```python
from UES_P01 import protect_image, restore_image

key = "image-protection-key"

# Convert original image into an anti-crawler grayscale noise map
protect_result = protect_image("input.png", "protected.png", key)

# Restore noise map back to original RGBA image
restore_result = restore_image("protected.png", "restored.png", key)
```

---

## Technical Limitations & Notes

1. **D01 Capacity Limit**: `UES-D01` requires text compressed via `zlib` to not exceed 63 bytes. For longer data, please use `UES-D02`.
2. **Key Precision**: Encryption and decryption heavily rely on the PRNG seed derived from the key. If the key differs by even 1 bit, decompression will fail.
3. **Cryptographic Security Positioning**: The core purpose of this project is **data steganography, obfuscation, and anti-AI automated harvesting**. System randomness relies on Mersenne Twister (MT19937) / 
Pseudo-RNG algorithms and should not replace standard cryptographic algorithms like AES for high-security financial transmission.


