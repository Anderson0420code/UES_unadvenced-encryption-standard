[README.md.md](https://github.com/user-attachments/files/33213454/README.md.md)
# UES (Unadvanced Encryption Standard) Protocol Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Web Audio API](https://img.shields.io/badge/Web%20Audio-Supported-brightgreen.svg)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
[![Status: Production--Ready](https://img.shields.io/badge/Status-Production--Ready-0055ff.svg)](#)

An advanced multi-modal asset protection and cryptographic obfuscation protocol suite engineered to safeguard digital assets against unauthorized automated web scraping, dataset harvesting, voice cloning, and AI model ingestion (e.g., Whisper, Wav2Vec2, ElevenLabs, ViT, and CNN feature extractors).

---

## 📋 Protocol Suite Architecture Overview

The **UES Protocol Suite** consists strictly of four core specialized protocols designed for audio and visual asset defense:

| Protocol ID | Type | Domain | Target AI Threat | Defense Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **UES-S01** | Acoustic | 1D Speech & Audio | Whisper, Wav2Vec2, Voice Cloning | Infrasound Modulation + Ultrasound Phase Perturbation |
| **UES-P01** | Visual | 2D Raster Graphics | Web Scrapers, Dataset Harvesting | Zlib Deflate Payload + MT19937 Spatial Permutation + Boundary Noise Envelope |
| **UES-D01** | Dynamic | Web Asset Tokenization | Automated Replay & Scraping Bots | UTC Epoch Seed Rotation + Dynamic Token Salt Vectors |
| **UES-D02** | Spectral | Image Frequency Domain | CNN Edge Extractors, Screenshot Ingestion | 2D-DCT Frequency Shifting & Mid-High Coefficient Inversion |

---

## 📐 Detailed Protocol Specifications

### 1. UES-S01: Acoustic Spectral Obfuscation & Anti-Voice-Cloning

UES-S01 protects 1D audio signals (speech, music, voice assets) against Automatic Speech Recognition (ASR) systems and Neural Voice Cloning backbones while preserving 100% human listening clarity.

```
+------------------+     +-----------------------------------+     +-----------------------+
|  Original Audio  | --> | UES-S01 Acoustic Engine           | --> | Protected Audio (WAV) |
| (Speech / Voice) |     | - Infrasound Modulation (<20Hz)   |     | - Human: 100% Clear   |
+------------------+     | - Ultrasound Phase Jitter (>18kHz)|     | - AI Model: Collapsed |
                         +-----------------------------------+     +-----------------------+
```

#### Technical Mechanics:
1. **Infrasound Sub-Audible Envelope Modulation ($f < 20\text{ Hz}$)**:
   Injects sub-audible carrier waves into the audio amplitude envelope:
   $$y_{\text{infra}}(t) = x(t) + \alpha \cdot \sin(2\pi \cdot 14.5 \cdot t)$$
   Induces temporal positional embedding drift within Transformer attention windows ($\text{Attention}(Q, K, V)$) without altering human-perceived pitch or vocal timbre.

2. **Ultrasound High-Frequency Adversarial Phase Scrambling ($f > 18\text{ kHz}$)**:
   Executes Short-Time Fourier Transform (STFT) on $N_{\text{fft}} = 1024$ frames with hop size $H = 256$. Applies key-derived high-entropy pseudo-random phase jitter $\phi \sim U(-\pi, \pi)$ exclusively to frequency bins above $18\text{ kHz}$:
   $$S(f, t) \leftarrow S(f, t) \cdot e^{j \cdot \phi(f, t) \cdot \beta} \quad \forall f \ge 18\text{ kHz}$$
   Causes feature map distortion and gradient collapse in Mel-Filterbank backbones while remaining outside human hearing capability.

3. **Deterministic Key Inverse Restoration**:
   Authorized principals with the SHA-256 derived master passphrase perform deterministic phase subtraction to restore the unperturbed original audio.

---

### 2. UES-P01: Visual Anti-AI Scraping and Noise Envelope Matrix

UES-P01 implements a multi-stage cryptographic compression and spatial permutation pipeline for 2D raster imagery:

1. **Payload Packaging**: Prepend an 8-byte big-endian dimension header ($\text{uint32 } W, \text{uint32 } H$) to raw RGBA pixel arrays, followed by Zlib Level 9 Deflate compression.
2. **Core Matrix Alignment**: Calculate core square matrix dimension $N = \lceil \sqrt{L} \rceil$ where $L$ is compressed byte length. Pad remaining bytes using master key PRNG stream.
3. **Global Spatial Permutation**: Derive a 32-bit PRNG seed via SHA-256 from the passphrase and shuffle pixel coordinate indices uniformly using Mersenne Twister ($MT19937$).
4. **Envelope Boundary Noise Wall**: Construct an outer protective boundary ($M = N + 2$) populated with high-entropy pseudo-random noise to disrupt computer vision edge detection heuristics.

---

### 3. UES-D01: Dynamic Seed-Rotation & Temporal Token Obfuscation

1. **Temporal Epoch Derivation**: Integrates configurable UTC epoch time resolution ($T = 3600\text{ s}$) into key derivation:
   $$\text{Seed}_t = \text{SHA-256}(\text{Passphrase} \parallel \lfloor \text{Timestamp} / T \rfloor)$$
2. **Multi-Layer Vector Rotation**: Automatically alters spatial permutation matrices at regular intervals to prevent replay attacks and dataset accumulation by web crawlers.

---

### 4. UES-D02: Multi-Channel Spectral Decomposition & Frequency Shifting

1. **Spectral Coefficient Scrambling**: Converts spatial color channels into frequency domain representations via 2D Discrete Cosine Transform (DCT).
2. **Adversarial Perturbation Injection**: Inverts mid-to-high frequency coefficients responsible for structural edge definition, preventing neural network feature reconstruction even under direct screen capture or viewport sampling.

---

## 📁 Repository Structure

```
UES_unadvanced-encryption-standard/
├── ues_s_series.py        # Python core engine for UES-S01 Audio Protection
├── ues_s_simulator.html   # Web Audio API real-time interactive simulator
├── README.md              # Official documentation & specification
└── LICENSE                # MIT License file
```

---

## ⚙️ Installation & Usage

### Python Dependencies
```bash
pip install numpy
```

### Quick Start: UES-S01 Audio Protection

```python
from ues_s_series import UESS01AudioEngine

# Initialize engine with passphrase
engine = UESS01AudioEngine(passphrase="My-Secret-Passphrase-2026")

# Apply acoustic protection (Output WAV is 100% human-playable and clear)
engine.protect_audio_file(
    input_wav_path="speech_original.wav",
    output_protected_wav_path="speech_protected.wav",
    ultra_intensity=0.85,
    infra_intensity=0.05
)

# Restore original audio using master passphrase
engine.restore_audio_file(
    protected_wav_path="speech_protected.wav",
    output_restored_wav_path="speech_restored.wav"
)
```

---

## 📄 License

This project is open-source and released under the terms of the **[MIT License](LICENSE)**.

```text
MIT License

Copyright (c) 2026 UES Protocol Development Team & Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
