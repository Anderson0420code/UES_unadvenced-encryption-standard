[official_readme_license.md](https://github.com/user-attachments/files/33296785/official_readme_license.md)
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
| **UES-S01** | Acoustic | 1D Speech & Audio | Gemini, Whisper, Wav2Vec2, Voice Cloning | In-Band Formant Masking ($200\text{Hz}-4\text{kHz}$) + Psychoacoustic Dynamic Noise |
| **UES-P01** | Visual | 2D Raster Graphics | Web Scrapers, Dataset Harvesting | Zlib Deflate Payload + MT19937 Spatial Permutation + Boundary Noise Envelope |
| **UES-D01** | Dynamic | Web Asset Tokenization | Automated Replay & Scraping Bots | UTC Epoch Seed Rotation + Dynamic Token Salt Vectors |
| **UES-D02** | Spectral | Image Frequency Domain | CNN Edge Extractors, Screenshot Ingestion | 2D-DCT Frequency Shifting & Mid-High Coefficient Inversion |

---

## 📐 Detailed Protocol Specifications

### 1. UES-S01: In-Band Psychoacoustic Acoustic Defense

Legacy ultrasound ($>18\text{kHz}$) defenses fail because AI Speech-to-Text (STT) pipelines apply anti-aliasing low-pass filters and downsample audio to $16\text{kHz}$, stripping high frequencies automatically.

**UES-S01** solves this by injecting adversarial perturbations directly into the active human speech band ($200\text{Hz} \le f \le 4000\text{Hz}$). It leverages the human auditory system's **psychoacoustic masking curve** so human listeners hear clean, natural speech, while AI Mel-Filterbank representations and Transformer Cross-Attention mechanisms suffer complete feature alignment collapse.

```
+------------------+     +-----------------------------------+     +-----------------------+
|  Original Audio  | --> | UES-S01 Acoustic Engine           | --> | Protected Audio (WAV) |
| (Speech / Voice) |     | - Speech Band Masking (200-4000Hz)|     | - Human: 100% Clear   |
+------------------+     | - Dynamic Energy Masking Threshold|     | - AI Model: Collapsed |
                         +-----------------------------------+     +-----------------------+
```

#### Technical Mechanics:

1. **Short-Time Fourier Transform (STFT) Formant Target**:
   Given discrete audio sample sequence $x[n]$, compute frame-level complex spectrum $S(f, t)$ with window length $N_{\text{fft}} = 1024$ and hop size $H = 256$:
   $$S(f, t) = \text{STFT}\{x[n]\}$$

2. **In-Band Adversarial Phase Scrambling**:
   Apply key-derived phase perturbation $\phi(f, t) \sim U(-\pi, \pi)$ exclusively across human speech formant frequencies ($200\text{Hz} \le f \le 4000\text{Hz}$):
   $$S_{\text{perturbed}}(f, t) = |S(f, t)| \cdot \exp\left(j \cdot \left( \angle S(f, t) + \alpha \cdot \phi(f, t) \cdot \mathbb{I}_{200 \le f \le 4000} \right)\right)$$
   where $\alpha$ is the in-band perturbation intensity parameter ($0.0 \le \alpha \le 1.0$).

3. **Psychoacoustic Dynamic Energy Masking**:
   Adversarial noise magnitude $N_{\text{mask}}(f, t)$ is scaled relative to the instantaneous frame spectral energy $E(t) = \frac{1}{K} \sum_{k} |S(k, t)|$:
   $$N_{\text{mask}}(f, t) = |S(f, t)| \cdot \lambda \cdot \mathcal{N}(0, 1) \cdot \mathbb{I}_{200 \le f \le 4000}$$
   where $\lambda$ represents the masking threshold coefficient.

4. **Resilience Guarantee**:
   Because perturbations reside strictly within $200\text{Hz} - 4000\text{Hz}$, they remain intact after $16\text{kHz}$ ASR downsampling, MP3/AAC lossy compression, and bandpass filtering.

---

### 2. UES-P01: Visual Anti-AI Scraping & Noise Envelope Matrix

UES-P01 transforms standard 2D raster images into cryptographically secure, visually obfuscated noise envelope matrices to block automated image scraping and vision-language model (VLM) training dataset compilation.

#### Technical Pipeline:

1. **Payload Packaging**:
   Extract raw RGBA pixel bytes $P$, prepend an 8-byte big-endian dimension header ($\text{uint32 } W, \text{uint32 } H$), and apply Zlib Level 9 Deflate compression:
   $$C = \text{Deflate}_{\text{lvl9}}(\text{Header}(W, H) \mathbin{\Vert} P)$$

2. **Core Matrix Construction ($N \times N$)**:
   Determine minimum square matrix dimension $N$:
   $$N = \lceil \sqrt{|C|} \rceil$$
   Pad remaining array entries with pseudo-random bytes derived from master seed $K_{\text{master}}$ to form matrix $\mathbf{M}_{\text{core}} \in \mathbb{R}^{N \times N}$.

3. **Mersenne Twister (MT19937) Spatial Permutation**:
   Derive a 32-bit seed using SHA-256:
   $$\text{Seed} = \text{uint32}(\text{SHA-256}(\text{Passphrase})[0:4])$$
   Uniformly scramble $1\text{D}$ coordinate indices across $\mathbf{M}_{\text{core}}$ using pseudo-random index mapping $\pi_{\text{Seed}}(i)$.

4. **Envelope Boundary Noise Wall ($M \times M$)**:
   Expand matrix dimensions to $M = N + 2r$ with boundary thickness $r = 1$. Fill outer boundary cells with high-entropy pseudo-random noise to disrupt computer vision edge detection heuristics (e.g., Canny, Sobel) and feature extractors.

---

### 3. UES-D01: Dynamic Seed-Rotation & Temporal Token Obfuscation

UES-D01 prevents replay attacks and cumulative dataset scraping by updating permutation matrices according to a temporal epoch clock.

1. **Temporal Epoch Key Derivation**:
   Given time step window $T = 3600\text{ seconds}$ (1 hour), calculate the epoch-specific seed:
   $$\text{Seed}_t = \text{SHA-256}\left( \text{Passphrase} \mathbin{\Vert} \left\lfloor \frac{\text{Timestamp}_{\text{UTC}}}{T} \right\rfloor \right)$$

2. **Multi-Layer Vector Rotation**:
   Re-indexes spatial permutations dynamically. Even if an adversary captures protected web assets over time, the index alignment continuously shifts, invalidating offline dataset aggregation.

---

### 4. UES-D02: Multi-Channel Spectral Decomposition & Frequency Shifting

UES-D02 targets Discrete Cosine Transform (DCT) coefficients in raster imagery to defeat neural network feature reconstruction under direct screenshot or viewport capture conditions.

1. **Frequency Domain Transformation**:
   Convert spatial color channels into frequency domain representations via 2D-DCT over $8 \times 8$ blocks:
   $$\mathbf{D} = \text{DCT-2D}(\mathbf{I}_{8 \times 8})$$

2. **Mid-High Coefficient Inversion**:
   Invert and shuffle mid-to-high frequency coefficients responsible for structural edge definition:
   $$\mathbf{D}_{\text{modified}}(u, v) = -\mathbf{D}(u, v) \cdot \beta(u, v) \quad \forall (u, v) \in \text{Mid-High Frequencies}$$

3. **Adversarial Gradient Distortion**:
   Induces classification collapse in Convolutional Neural Networks (CNNs) and Vision Transformers (ViTs) while maintaining authorized key-based reconstruction fidelity.

---

## 📁 Repository File Structure

```text
UES_unadvanced-encryption-standard/
├── ues_s_series.py        # Python core engine for UES-S01 Audio Defense
├── ues_s_simulator.html   # Web Audio API real-time interactive simulator & exporter
├── README.md              # Official protocol suite documentation & license
└── LICENSE                # MIT License file
```

---

## ⚙️ Quick Start & Installation

### Prerequisites

```bash
# Clone the official repository
git clone https://github.com/Anderson0420code/UES_unadvanced-encryption-standard.git
cd UES_unadvanced-encryption-standard

# Install required Python dependencies
pip install numpy
```

---

### Python Code Example (UES-S01 Audio Protection)

```python
from ues_s_series import UES_S01_AudioEngine

# Initialize the engine with a passphrase
engine = UES_S01_AudioEngine(passphrase="Secret-Audio-Passphrase-2026")

# Apply UES-S01 In-Band Psychoacoustic Defense
# Output file is directly playable by humans, but triggers AI STT failure
engine.protect_audio_file(
    input_wav_path="original_speech.wav",
    output_protected_wav_path="protected_speech_inband.wav",
    inband_intensity=0.45,       # Formant perturbation scale (200Hz - 4kHz)
    masking_threshold=0.15       # Psychoacoustic dynamic energy masking
)

# Restore original audio via key-derived phase subtraction
engine.restore_audio_file(
    protected_wav_path="protected_speech_inband.wav",
    output_restored_wav_path="restored_speech.wav"
)
```

---

### Interactive Web Simulator (`ues_s_simulator.html`)

Open `ues_s_simulator.html` in any modern web browser (Chrome, Firefox, Edge, Safari) to access the interactive workbench:

* **Real-Time Web Audio Engine**: Synthesize voice or upload custom `.wav` / `.mp3` files.
* **4-Panel Visualizer Grid**: Live preview of Waveforms, $200\text{Hz}-4\text{kHz}$ In-Band Spectrograms, Human Hearing Perception Curves, and AI Mel-Filterbank Feature Alignment maps.
* **WAV Export**: Direct client-side generation and download of protected $16\text{-bit}$ PCM `.wav` audio files.

---

## 📄 License

This project is licensed under the terms of the **[MIT License](LICENSE)**.

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
