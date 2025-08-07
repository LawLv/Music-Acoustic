import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import simpleaudio as sa
import os

# Sampling rate and duration
fsamp = 32000  # 32kHz sampling rate
total_time = 5  # 5 seconds

# Vibrato parameters
vib_amp = 0.001
vib_freq = 6

A = -0.8


# Source signal generation
def generate_source(f0, slope=-6):
    t = np.linspace(0, total_time, int(total_time * fsamp))
    vib = (1 + (vib_amp / (t + 1e-5)) * np.sin(2 * np.pi * vib_freq * t)) * f0
    N_harmonics = min(30, int(fsamp / (2 * f0)))  # Limit harmonics to Nyquist
    source = np.zeros_like(t)
    for i in range(1, N_harmonics + 1):
        source += A * (i ** (slope / 6)) * np.sin(2 * np.pi * i * vib * t)
    return source


# Resonance filter design
def resonance_filter(input_signal, fN, bN):
    T = 1 / fsamp
    output_signal = np.copy(input_signal)
    for f, b in zip(fN, bN):
        q = f / b
        beta = f * 2 * np.pi
        beta0 = beta * np.sqrt(1 + 1 / (4 * q ** 2))
        alpha = beta0 / (2 * q)
        a1 = -2 * np.exp(-alpha * T) * np.cos(beta * T)
        a2 = np.exp(-2 * alpha * T)
        G = 1 + a1 + a2
        output_signal = lfilter([G], [1, a1, a2], output_signal)
    return output_signal


# Formant data (from measured values)
vowel_data = {
    'a': [105, [840, 1360, 2520, 3640, 5000], [60, 80, 100, 120, 140]],
    'o': [103, [320, 760, 3240, 4240, 7080], [60, 80, 100, 120, 140]],
    'e': [104, [560, 1240, 2600, 3400, 4480], [50, 70, 90, 110, 130]],
    'i': [105, [360, 2200, 2800, 3600, 4400], [50, 70, 90, 110, 130]],
    'u': [107, [360, 800, 2160, 3520, 4320], [45, 65, 85, 105, 125]],
    'v': [105, [320, 1800, 2440, 3440, 4440], [45, 65, 85, 105, 125]]
}


# Generate and filter speech sound
def synthesize_vowel(vowel, volume=0.01):
    f0, formants, bandwidths = vowel_data[vowel]
    source = generate_source(f0)
    filtered = resonance_filter(source, formants, bandwidths)
    return filtered * volume


# Plot spectrogram
def plot_spectrogram(signal, title):
    plt.figure(figsize=(10, 4))
    plt.specgram(signal, Fs=fsamp, NFFT=1024, noverlap=512, cmap='inferno')
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Intensity (dB)")
    plt.savefig(os.path.join(os.getcwd(), title), dpi=300)
    plt.show()


# Generate a melody (changing pitch and vowels)
def generate_melody():
    melody = [('a', 1.0), ('o', 1.2), ('e', 0.8), ('i', 1.0), ('u', 1.1), ('v', 0.9)]
    full_signal = np.array([])
    for vowel, speed in melody:
        synth = synthesize_vowel(vowel)
        synth = signal.resample(synth, int(len(synth) / speed))  # Adjust duration
        full_signal = np.concatenate((full_signal, synth))
    return full_signal


# Generate and play audio
def play_audio(signal):
    signal = (signal * 32767).astype(np.int16)
    wav.write("synthesized_speech.wav", fsamp, signal)
    wave_obj = sa.WaveObject(signal, num_channels=1, bytes_per_sample=2, sample_rate=fsamp)
    play_obj = wave_obj.play()
    play_obj.wait_done()


# Run synthesis and plot results
if __name__ == "__main__":
    # Select a vowel and synthesize it
    vowel = 'a'  # Try different vowels
    speech_signal = synthesize_vowel(vowel)
    plot_spectrogram(speech_signal, title=f"Spectrogram of Synthesized '{vowel}'")

    # Generate melody
    melody_signal = generate_melody()
    plot_spectrogram(melody_signal, title="Spectrogram of Synthesized Melody")

    # Play synthesized sound
    play_audio(melody_signal)
