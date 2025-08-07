import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import librosa
import librosa.display
import matplotlib.pyplot as plt
import sounddevice as sd
import os
import soundfile as sf


# Task 1: Read audio and draw the waveform
def plot_waveform(filename, title):
    audio, sr = librosa.load(filename, sr=None)
    # Generate timeline
    t = np.linspace(0, len(audio) / sr, len(audio))
    # Draw a waveform
    plt.figure(figsize=(10, 4))
    plt.plot(t, audio, label=title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.legend()

    # Save image
    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_filename = f"{base_name}_waveform.png"
    plt.savefig(output_filename, dpi=300)
    plt.show()

    return sr, audio


# Task 2: Compute the STFT magnitude spectrum and find the partial tones
def analyze_spectrum(filename,audio, sr, times, win_size=0.1, max_freq=15000):
    base_name = os.path.splitext(os.path.basename(filename))[0]
    n_fft = int(win_size * sr)  # 100ms window
    hop_length = n_fft // 2
    #  Complex spectrum matrix
    f, t, Zxx = signal.stft(audio, sr, nperseg=n_fft, noverlap=hop_length, window="boxcar")
    all_peaks = []

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(20 * np.log10(np.abs(Zxx) + 1e-10), sr=sr, hop_length=hop_length, x_axis="time", y_axis="log")
    plt.colorbar(label="Magnitude (dB)")
    plt.title(f"Spectrogram of {base_name}")  # 显示文件名
    output_filename = f"{base_name}_spectrogram.png"
    plt.savefig(output_filename, dpi=300)  # 保存图片
    plt.show()

    # 选择两个时间点进行频谱分析
    for t_idx, time in enumerate(times):
        idx = np.argmin(np.abs(t - time))
        spectrum = np.abs(Zxx[:, idx])

        # Choose < 15kHz
        valid_indices = f <= max_freq
        valid_frequencies = f[valid_indices]
        valid_spectrum = spectrum[valid_indices]

        peak_indices = signal.find_peaks(valid_spectrum)[0]  # 选取能量最高的峰值
        peaks = sorted(zip(valid_frequencies[peak_indices], valid_spectrum[peak_indices]), key=lambda x: -x[1])[ :5]  # 取前5个部分音
        all_peaks.append(peaks)

        # Plot magnitude spectrum
        plt.figure(figsize=(10, 4))
        plt.plot(valid_frequencies, valid_spectrum, label=f"{time}s Window")
        plt.scatter([p[0] for p in peaks], [p[1] for p in peaks], color='red', label='Peaks')
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.title(f"Magnitude Spectrum at {time}s")
        plt.legend()
        plt.grid()

        output_filename = f"{base_name}_magnitude_spectrum_{t_idx}.png"
        plt.savefig(output_filename, dpi=300)
        plt.show()


        print(f"Time {time:.3f}s for {base_name}: Top Partials (Freq, Amplitude)")
        for freq, amp in peaks:
            print(f"  {freq:.1f} Hz, {amp:.5f}")

    return all_peaks




# 任务 3: Estimate exponential amplitude envelope
def estimate_and_plot_envelopes(filename, all_peaks, times):
    base_name = os.path.splitext(os.path.basename(filename))[0]
    plt.figure(figsize=(8, 5))
    A_values = []
    gamma_values = []

    # Fixed analysis of the harmonics at the first time point
    reference_partials = [peak[0] for peak in all_peaks[0]]  # 取第一个时间点的泛音频率

    print(f"{base_name}: Top Partials: (A, gamma)")
    for ref_freq in reference_partials: # 对于每个频率
        amplitudes = []
        for j in range(len(times)):
            # 查找该时间点是否检测到相同频率的泛音
            found = False
            for peak in all_peaks[j]:
                if abs(peak[0] - ref_freq) < 20:  # 允许微小频率偏差匹配
                    amplitudes.append(peak[1])
                    found = True
                    break
            if not found:
                amplitudes.append(0)  # 该时间点未检测到该泛音，设为 0

        times_arr = np.array(times)
        amplitudes_arr = np.array(amplitudes)

        # 过滤掉 0 振幅，避免 log(0) 错误
        valid_idx = amplitudes_arr > 0
        if np.sum(valid_idx) < 2:
            continue  # 至少需要两个有效点

        times_valid = times_arr[valid_idx]
        amplitudes_valid = amplitudes_arr[valid_idx]
        log_amplitudes = np.log(amplitudes_valid)
        gamma_n = -np.polyfit(times_valid, log_amplitudes, 1)[0]
        A_n = np.exp(np.polyfit(times_valid, log_amplitudes, 1)[1])

        A_values.append(A_n)
        gamma_values.append(gamma_n)

        t_fit = np.linspace(0, max(times), 100)
        envelope = A_n * np.exp(-gamma_n * t_fit)

        plt.plot(t_fit, envelope, label=f"Partial {ref_freq:.1f} Hz")
        plt.scatter(times_valid, amplitudes_valid, color='red')
        print(f"Partial {ref_freq:.1f} Hz: A = {A_n:.4f}, gamma = {gamma_n:.4f}")

    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Estimated Exponential Envelopes")
    plt.legend()
    plt.grid()
    output_filename = f"{base_name}_envelopes.png"
    plt.savefig(output_filename, dpi=300)
    plt.show()

    return A_values, gamma_values


# 任务 4: 加性合成
def synthesize_sound(filename, sr, duration, reference_partials, A_values, gamma_values):
    base_name = os.path.splitext(os.path.basename(filename))[0]
    t = np.linspace(0, duration, int(sr * duration))
    synthesized_wave = np.zeros_like(t)

    for i in range(len(reference_partials)):
        env = A_values[i] * np.exp(-gamma_values[i] * t)
        synthesized_wave += env * np.sin(2 * np.pi * reference_partials[i] * t)

    # 标准化音频
    synthesized_wave /= np.max(np.abs(synthesized_wave))

    output_filename = base_name + "_synthesized.wav"
    sf.write(output_filename, synthesized_wave, sr)
    print(f"Synthesized audio saved as {output_filename}")

    return synthesized_wave


# 任务 5: 生成旋律
def play_melody(filename, sr, note_durations, scale_intervals, reference_partials, A_values, gamma_values):
    melody_wave = []
    base_name = os.path.splitext(os.path.basename(filename))[0]

    for interval, duration in zip(scale_intervals, note_durations):
        transposed_partials = [freq * (2 ** (interval / 12)) for freq in reference_partials]  # 音高变换
        note_wave = synthesize_sound(filename, sr, duration, transposed_partials, A_values, gamma_values)
        melody_wave.append(note_wave)

    melody_wave = np.concatenate(melody_wave)
    melody_wave /= np.max(np.abs(melody_wave))  # 标准化

    output_filename = base_name + "_melody.wav"
    sf.write(output_filename, melody_wave, sr)
    print(f"Melody audio saved as {output_filename}")

    return melody_wave



# --------------- Run a full analysis -----------------
# Select two Glockenspiel audios
file1 = "A2-Glockenspiel-samples/A2-Glockenspiel-samples/Gsp_ME_f_L-sus_F#5.wav"
file2 = "A2-Glockenspiel-samples/A2-Glockenspiel-samples/Gsp_ME_f_L-sus_F#6.wav"

# 任务 1: 绘制波形
print("Task 1")
sr1, audio1 = plot_waveform(file1, "Glockenspiel F#5")
sr2, audio2 = plot_waveform(file2, "Glockenspiel F#6")

# 任务 2: 频谱分析
print("Task 2")
peaks_file1 = analyze_spectrum(file1 ,audio1, sr1, times=[0.02, 0.6])
peaks_file2 = analyze_spectrum(file2 ,audio2, sr2, times=[0.02, 0.6])

# 任务 3: 估计指数包络
print("Task 3")
A_values_file1, gamma_values_file1 = estimate_and_plot_envelopes(file1, peaks_file1, times=[0.02, 0.6])
A_values_file2, gamma_values_file2 = estimate_and_plot_envelopes(file2, peaks_file2, times=[0.02, 0.6])

# 任务 4: 加性合成
print("Task 4")
synthesized_audio1 = synthesize_sound(file1, sr1, duration=2, reference_partials=[12960, 9460, 5520], A_values=[0.0393, 0.0333, 0.0214], gamma_values=[7.2606, 5.3482, 2.4321])
synthesized_audio2 = synthesize_sound(file2, sr2, duration=2, reference_partials=[7710, 7910, 1480, 12510], A_values=[0.0396, 0.0117, 0.0090, 0.0076], gamma_values=[9.6857, 3.9471, -0.4151, 5.7185])

# 保存合成音频
print("Task 5")
melody_wave1 = play_melody(file1, sr1,
                          note_durations=[0.5, 0.5, 1.0, 1.0, 1.0, 2.0],
                          scale_intervals=[0, 0, 2, 0, 6, 5],
                          reference_partials=[12960, 9460, 5520],
                          A_values=[0.0393, 0.0333, 0.0214],
                          gamma_values=[7.2606, 5.3482, 2.4321])
melody_wave2 = play_melody(file2, sr2,
                          note_durations=[0.5, 0.5, 1.0, 1.0, 1.0, 2.0],
                          scale_intervals=[0, 0, 2, 0, 6, 5],
                          reference_partials=[7710, 7910, 1480, 12510],
                          A_values=[0.0396, 0.0117, 0.0090, 0.0076],
                          gamma_values=[9.6857, 3.9471, -0.4151, 5.7185])


