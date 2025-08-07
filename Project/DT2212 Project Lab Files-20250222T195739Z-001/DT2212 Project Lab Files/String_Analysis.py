import numpy as np
import scipy.signal as signal
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os

from numba.core.ir import Print


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
    output_dir = os.path.dirname(filename)
    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_filename = os.path.join(output_dir, f"{base_name}_waveform.png")
    plt.savefig(output_filename, dpi=300)

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
    output_dir = os.path.dirname(filename)
    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_filename = os.path.join(output_dir, f"{base_name}_spectrogram.png")
    plt.savefig(output_filename, dpi=300)  # 保存图片

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

        # 标注每个峰值的频率
        for freq, magnitude in peaks:
            plt.annotate(f"{freq:.1f} Hz",  # 保留一位小数
                         xy=(freq, magnitude),
                         xytext=(0, 5),  # 文字偏移量
                         textcoords='offset points',
                         ha='center', fontsize=8, color='blue')

        plt.xlim(0, 4000)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.title(f"Magnitude Spectrum at {time}s")
        plt.legend()
        plt.grid()

        output_dir = os.path.dirname(filename)
        base_name = os.path.splitext(os.path.basename(filename))[0]
        output_filename = os.path.join(output_dir, f"{base_name}_magnitude_spectrum_{t_idx}.png")
        plt.savefig(output_filename, dpi=300)



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

    output_dir = os.path.dirname(filename)
    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_filename = os.path.join(output_dir, f"{base_name}_envelopes.png")
    plt.savefig(output_filename, dpi=300)


    return A_values, gamma_values


# Task 4
def cal_inharmonicity(filename, all_peaks, f_0=None, tolerance=0.05):
    # 提取第一个时间点的频率
    detected_freqs = [peak[0] for peak in all_peaks[0]]

    # 如果未提供基频，则取最小值为基频
    if f_0 is None:
        f_0 = min(detected_freqs)
        print(f"Estimated fundamental frequency (f_0): {f_0:.2f} Hz")
    else:
        print(f"Using provided fundamental frequency (f_0): {f_0:.2f} Hz")

    B_values = []
    harmonic_numbers = []

    for f_n in detected_freqs:
        # 估算泛音阶数
        n_est = round(f_n / f_0)

        # 忽略无效或基频阶数
        if n_est < 2: continue

        # 验证检测频率是否接近预测频率
        predicted_freq = n_est * f_0
        freq_error = abs(f_n - predicted_freq) / predicted_freq

        if freq_error <= tolerance:
            # 计算非谐性系数 B
            B_n = ((f_n / (n_est * f_0)) ** 2 - 1) / (n_est ** 2)
            B_values.append(B_n)
            harmonic_numbers.append(n_est)
            print(f"Harmonic {n_est}: Detected {f_n:.2f} Hz, Predicted {predicted_freq:.2f} Hz, B = {B_n:.6f}")
        else:
            print(f"Harmonic {n_est} skipped: Detected {f_n:.2f} Hz differs by {freq_error*100:.2f}% from predicted {predicted_freq:.2f} Hz")

    # 计算平均 B
    B_avg = np.nanmean(B_values) if B_values else 0
    print(f"\nAverage Inharmonicity Coefficient (B): {B_avg:.6f}")

    # 绘制 B 随泛音阶数变化图
    if B_values:
        # 将 harmonic_numbers 和 B_values 按 harmonic_numbers 升序排序
        sorted_pairs = sorted(zip(harmonic_numbers, B_values), key=lambda x: x[0])
        harmonic_numbers, B_values = zip(*sorted_pairs)  # 解压为两个有序列表

        plt.figure(figsize=(10, 6))
        plt.plot(harmonic_numbers, B_values, 'o-', label='Inharmonicity Coefficient B')
        plt.xlabel("Harmonic Number")
        plt.ylabel("B Value")
        plt.title(f"Inharmonicity for {filename}")
        plt.grid(True)
        plt.legend()

        output_dir = os.path.dirname(filename)
        base_name = os.path.splitext(os.path.basename(filename))[0]
        output_filename = os.path.join(output_dir, f"Inharmonicity for {base_name}")
        plt.savefig(output_filename, dpi=300)
        plt.show()

        # save B_values
        file_name = 'B_values.txt'
        with open(file_name, 'a') as f:
            # 将 B_values 转换为字符串，并以逗号分隔写入一行
            f.write(','.join(map(str, harmonic_numbers)) + '\n')
            f.write(','.join(map(str, B_values)) + '\n')

    return B_avg, B_values


# --------------- Run a full analysis -----------------
Flatwound = "Flatwound/Flatwound_Strong.wav"  # [0.4, 1.2], f_0 = 73.42
Gut = "Gut/Gut_Strong.wav"  # [0.4, 1.2], f_0 = 146.83
Nylgut = "Nylgut/Nylgut_Strong.wav"  # [0.4, 1.2], f_0 = 146.83
Nylgut_wound = "Nylgut(wound)/Nylgut(wound)_Strong.wav"  # [0.4, 1.2], f_0 = 73.42
Nylon = "Nylon/Nylon_Strong.wav"  # [0.6, 1.2], f_0 = 146.83
Nylon_wound = "Nylon(wound)/Nylon(wound)_Strong.wav"  # [0.3, 1.3], f_0 = 73.42
Roundwound = "Roundwound/Roundwound_Strong.wav"  # [0.5, 1.3], f_0 = 73.42
Silk_wound = "Silk(wound)/Silk(wound)_Strong.wav"  # [0.5, 1.3], f_0 = 73.42
Steel = "Steel/Steel_Strong.wav" # [0.4, 1.0], f_0 = 146.83

file1 = Steel

# 任务 1: 绘制波形
print("1. Plot Waveform")
sr1, audio1 = plot_waveform(file1, os.path.basename(file1))
print("--------------------------------------------------")

# 任务 2: 频谱分析
print("2. Analyze_Spectrum")
peaks_file1 = analyze_spectrum(file1 ,audio1, sr1, times=[0.4, 1.0])
print("--------------------------------------------------")

# 任务 3: 估计指数包络
print("3. Decay Rate")
A_values_file1, gamma_values_file1 = estimate_and_plot_envelopes(file1, peaks_file1, times=[0.4, 1.0])
print("--------------------------------------------------")

print("4. Inharmonicity Coefficient")
B_avg1, B_values1 = cal_inharmonicity(file1, peaks_file1, f_0 = 146.83, tolerance=0.1)

