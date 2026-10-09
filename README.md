[README.md](https://github.com/user-attachments/files/33237907/README.md)
# UES (Unadvanced Encryption Standard) Protocol Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Web Audio API](https://img.shields.io/badge/Web%20Audio-Supported-brightgreen.svg)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
[![Status: Production--Ready](https://img.shields.io/badge/Status-Production--Ready-0055ff.svg)](#)

An advanced multi-modal asset protection and cryptographic obfuscation protocol suite engineered to safeguard digital assets against unauthorized automated web scraping, dataset harvesting, voice cloning, and AI model ingestion (e.g., Whisper, Gemini Speech-to-Text, Wav2Vec2, ElevenLabs, ViT, and CNN feature extractors).

---

## 📋 Protocol Suite Architecture Overview

The **UES Protocol Suite** consists strictly of four core specialized protocols designed for audio and visual asset defense:

| Protocol ID | Type | Domain | Target AI Threat | Defense Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **UES-S01** | Acoustic | 1D Speech & Audio | Gemini, Whisper, Wav2Vec2, Voice Cloning | In-Band Formant Masking (200Hz-4kHz) + Psychoacoustic Dynamic Noise |
| **UES-P01** | Visual | 2D Raster Graphics | Web Scrapers, Dataset Harvesting | Zlib Deflate Payload + MT19937 Spatial Permutation + Boundary Noise Envelope |
| **UES-D01** | Dynamic | Web Asset Tokenization | Automated Replay & Scraping Bots | UTC Epoch Seed Rotation + Dynamic Token Salt Vectors |
| **UES-D02** | Spectral | Image Frequency Domain | CNN Edge Extractors, Screenshot Ingestion | 2D-DCT Frequency Shifting & Mid-High Coefficient Inversion |

---

## 📐 Detailed Protocol Specifications

### 1. UES-S01: In-Band Psychoacoustic Acoustic Defense

Unlike naive ultra/infrasound defenses that are automatically removed by AI pre-processing (downsampling to 16kHz and bandpass filtering), **UES-S01** targets the active human speech band ($200\text{Hz} - 4000\text{Hz}$) directly inside the Mel-Filterbank passband.

```
+------------------+     +-----------------------------------+     +-----------------------+
|  Original Audio  | --> | UES-S01 Acoustic Engine           | --> | Protected Audio (WAV) |
| (Speech / Voice) |     | - Speech Band Masking (200-4000Hz)|     | - Human: 100% Clear   |
+------------------+     | - Dynamic Energy Masking Threshold|     | - AI Model: Collapsed |
                         +-----------------------------------+     +-----------------------+
```

#### Technical Mechanics:
1. **Speech Formant Band Targeted Perturbation ($200\text{Hz} \le f \le 4000\text{Hz}$)**:
   Executes Short-Time Fourier Transform (STFT) with $N_{\text{fft}} = 1024$ and hop length $H = 256$. Injects phase perturbations $\phi \sim U(-\pi, \pi)$ directly into critical speech formant frequencies ($F_1, F_2, F_3$):
   $$S(f, t) \leftarrow S(f, t) \cdot e^{j \cdot \phi(f, t) \cdot \alpha} \quad \forall f \in [200\text{Hz}, 4000\text{Hz}]$$

2. **Psychoacoustic Temporal & Spectral Energy Masking**:
   Scales adversarial noise relative to frame-level spectral energy:
   $$N_{\text{mask}}(f, t) = |S(f, t)| \cdot \lambda \cdot \mathcal{N}(0, 1)$$
   The human auditory system hides the noise under prominent vocal formants (auditory masking curve), while AI Transformer Cross-Attention and Mel-Filterbank feature alignments collapse.

3. **Resilience to AI Downsampling & Filtering**:
   Because the perturbations reside within $200\text{Hz} - 4000\text{Hz}$, they survive $16\text{kHz}$ ASR audio downsampling, low-pass filtering, and MP3/AAC lossy compression.

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
├── ues_s_simulator.html   # Web Audio API real-time interactive simulator & WAV exporter
├── README.md              # Official documentation & specification
└── LICENSE                # MIT License file
```

---

## ⚙️ Quick Start

### Python Usage

```python
from ues_s_series import UES_S01_AudioEngine

# Initialize engine with passphrase
engine = UES_S01_AudioEngine(passphrase="Secret-Passphrase-2026")

# Generate protected audio file (Survives AI 16kHz downsampling)
engine.protect_audio_file(
    input_wav_path="input_speech.wav",
    output_protected_wav_path="protected_speech.wav",
    inband_intensity=0.45,
    masking_threshold=0.15
)

# Restore audio using key-derived phase subtraction
engine.restore_audio_file(
    protected_wav_path="protected_speech.wav",
    output_restored_wav_path="restored_speech.wav"
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
