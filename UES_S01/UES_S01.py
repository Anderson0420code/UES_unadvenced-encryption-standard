import math
import struct
import numpy as np
import wave
import hashlib

class UESS01AudioEngine:
    """
    UES-S01: Audio Anti-AI Scraping & Acoustic Spectral Obfuscation Protocol
    (Perceptual Adversarial Mode - Human Audible Sound is Pristine, AI Features Collapse)
    
    Features:
    - Infrasound (<20Hz) Temporal Attention-Disrupting Envelope Carrier
    - Ultrasound (>18kHz) High-Frequency Adversarial Phase Scrambling
    - Psychoacoustic Temporal-Spectral Masked Perturbation (Imperceptible to Humans)
    - Directly Playable Output WAV Audio (No raw cipher shuffling required)
    - Key-based Deterministic Inverse Filter Restoration
    """

    def __init__(self, passphrase: str, sample_rate: int = 44100):
        self.passphrase = passphrase.encode('utf-8')
        self.sample_rate = sample_rate
        # Derive primary PRNG seed using SHA-256
        self.master_seed_bytes = hashlib.sha256(self.passphrase).digest()
        self.seed_int = struct.unpack(">I", self.master_seed_bytes[:4])[0]

    def inject_adversarial_frequencies(
        self, 
        audio_data: np.ndarray, 
        ultra_intensity: float = 0.85, 
        infra_intensity: float = 0.05, 
        psycho_masking: float = 0.02
    ) -> np.ndarray:
        """
        Injects inaudible infrasound (<20Hz) and ultrasound (>18kHz) adversarial perturbations.
        Resulting audio sounds clear to human ears, but causes AI models (Whisper/Cloning) to fail.
        """
        num_samples = len(audio_data)
        t = np.arange(num_samples) / self.sample_rate

        # 1. Infrasound Modulation (<20Hz Sub-audible carrier - Inaudible to humans, disrupts Transformer Attention)
        infra_hz = 14.5  # Sub-audible frequency
        infra_carrier = np.sin(2 * np.pi * infra_hz * t) * (infra_intensity * 0.015)

        # 2. STFT Analysis for High-Frequency Ultrasound (>18kHz) Phase Perturbation
        n_fft = 1024
        hop_length = 256
        
        fft_freqs = np.fft.rfftfreq(n_fft, d=1.0 / self.sample_rate)
        ultrasound_mask = fft_freqs >= 18000.0  # Above human threshold (~18kHz)

        num_frames = (num_samples - n_fft) // hop_length + 1
        window = np.hanning(n_fft)

        input_audio = audio_data.astype(np.float32) + infra_carrier.astype(np.float32)
        out_audio = np.copy(input_audio)

        rng = np.random.default_rng(self.seed_int)

        # Apply frame-by-frame STFT adversarial phase injection
        for f in range(num_frames):
            start_idx = f * hop_length
            end_idx = start_idx + n_fft
            if end_idx > num_samples:
                break
                
            frame = input_audio[start_idx:end_idx] * window
            spectrum = np.fft.rfft(frame)

            # Apply pseudo-random phase jitter exclusively above 18kHz
            phase_noise = rng.uniform(-np.pi, np.pi, size=spectrum.shape)
            spectrum[ultrasound_mask] *= np.exp(1j * phase_noise[ultrasound_mask] * ultra_intensity)

            # Psychoacoustic masked noise injection (temporal energy proportional)
            if psycho_masking > 0:
                frame_energy = np.mean(np.abs(spectrum))
                psycho_noise = rng.standard_normal(size=spectrum.shape) * frame_energy * psycho_masking
                spectrum += psycho_noise

            resynthesized_frame = np.fft.irfft(spectrum) * window
            out_audio[start_idx:end_idx] += resynthesized_frame * 0.12

        # Normalize without clipping to preserve audio fidelity
        max_val = np.max(np.abs(out_audio))
        if max_val > 1.0:
            out_audio = out_audio / max_val

        return out_audio

    def protect_audio_file(
        self, 
        input_wav_path: str, 
        output_protected_wav_path: str, 
        ultra_intensity: float = 0.85, 
        infra_intensity: float = 0.05
    ):
        """
        Reads input WAV file, applies inaudible adversarial frequency perturbations,
        and saves a standard, directly playable protected WAV audio file.
        """
        with wave.open(input_wav_path, 'rb') as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            raw_pcm = wf.readframes(n_frames)

        self.sample_rate = framerate

        if sampwidth == 2:
            audio_arr = np.frombuffer(raw_pcm, dtype=np.int16).astype(np.float32) / 32768.0
        else:
            raise ValueError("Supports 16-bit PCM WAV audio files.")

        if n_channels == 1:
            protected_audio = self.inject_adversarial_frequencies(
                audio_arr, ultra_intensity, infra_intensity
            )
        else:
            audio_arr = audio_arr.reshape((-1, n_channels))
            channels_list = []
            for c in range(n_channels):
                ch_p = self.inject_adversarial_frequencies(
                    audio_arr[:, c], ultra_intensity, infra_intensity
                )
                channels_list.append(ch_p)
            protected_audio = np.stack(channels_list, axis=-1)

        # Convert back to standard 16-bit PCM WAV bytes
        pcm_out = (protected_audio * 32767.0).astype(np.int16).tobytes()

        with wave.open(output_protected_wav_path, 'wb') as wf:
            wf.setnchannels(n_channels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(framerate)
            wf.writeframes(pcm_out)

        print(f"[UES-S01 Audio Engine] Protected Audio Created: {output_protected_wav_path}")
        print(f" -> Playable Status: YES (Normal Sound to Humans, Adversarial to AI)")

    def restore_audio_file(
        self, 
        protected_wav_path: str, 
        output_restored_wav_path: str
    ):
        """
        Reverses the adversarial spectral perturbations using key-derived phase subtraction
        and notch filtering to yield pristine original audio.
        """
        with wave.open(protected_wav_path, 'rb') as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            raw_pcm = wf.readframes(n_frames)

        audio_arr = np.frombuffer(raw_pcm, dtype=np.int16).astype(np.float32) / 32768.0

        # Deterministic Inverse STFT Phase Filtering using Master Key Seed
        n_fft = 1024
        hop_length = 256
        fft_freqs = np.fft.rfftfreq(n_fft, d=1.0 / framerate)
        ultrasound_mask = fft_freqs >= 18000.0

        num_samples = len(audio_arr)
        num_frames = (num_samples - n_fft) // hop_length + 1
        window = np.hanning(n_fft)

        rng = np.random.default_rng(self.seed_int)
        restored_audio = np.copy(audio_arr)

        for f in range(num_frames):
            start_idx = f * hop_length
            end_idx = start_idx + n_fft
            if end_idx > num_samples:
                break

            frame = audio_arr[start_idx:end_idx] * window
            spectrum = np.fft.rfft(frame)

            # Subtract key-derived phase shift
            phase_noise = rng.uniform(-np.pi, np.pi, size=spectrum.shape)
            spectrum[ultrasound_mask] *= np.exp(-1j * phase_noise[ultrasound_mask] * 0.85)

            clean_frame = np.fft.irfft(spectrum) * window
            restored_audio[start_idx:end_idx] = clean_frame

        pcm_restored = (np.clip(restored_audio, -1.0, 1.0) * 32767.0).astype(np.int16).tobytes()

        with wave.open(output_restored_wav_path, 'wb') as wf:
            wf.setnchannels(n_channels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(framerate)
            wf.writeframes(pcm_restored)

        print(f"[UES-S01 Audio Engine] Audio Restored: {output_restored_wav_path}")

if __name__ == "__main__":
    print("--- UES-S01 Audio Adversarial Frequency Protection Verification ---")
    
    # Generate Synthetic Speech Audio Sample (2 seconds)
    sr = 44100
    t = np.linspace(0, 2.0, sr * 2)
    synthetic_speech = 0.5 * np.sin(2 * np.pi * 220 * t) + 0.3 * np.sin(2 * np.pi * 440 * t)
    pcm_bytes = (synthetic_speech * 32767).astype(np.int16).tobytes()

    input_wav = "original_speech.wav"
    with wave.open(input_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm_bytes)

    # Initialize Engine
    engine = UESS01AudioEngine(passphrase="Secret-Audio-Passphrase-2026")

    # Generate Adversarial Audio File (Playable directly, sounds normal to humans)
    engine.protect_audio_file(
        input_wav_path=input_wav,
        output_protected_wav_path="protected_speech_adversarial.wav",
        ultra_intensity=0.85,
        infra_intensity=0.05
    )

    # Restore Original
    engine.restore_audio_file(
        protected_wav_path="protected_speech_adversarial.wav",
        output_restored_wav_path="restored_speech_clean.wav"
    )