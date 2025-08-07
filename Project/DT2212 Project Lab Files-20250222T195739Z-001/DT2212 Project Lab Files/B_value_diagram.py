import os

import matplotlib.pyplot as plt

# 弦名称（按顺序）
string_names = [
    "Flatwound", "Gut", "Nylgut", "Nylgut(wound)", "Nylon",
    "Nylon(wound)", "Roundwound", "Silk(wound)", "Steel"
]

# 文件路径
file_path = 'B_values.txt'  # 确保该文件与脚本在同一目录下，或提供完整路径

# 读取文件中的9行数据
with open(file_path, 'r') as file:
    lines = file.readlines()

# 检查文件是否有正确的行数
if len(lines) != 18:
    raise ValueError("Should be 18 lines.")

# 解析数据，每两行为一组 (harmonic_numbers, B_values)
data_pairs = [
    (list(map(float, lines[i].strip().split(','))), list(map(float, lines[i + 1].strip().split(','))))
    for i in range(0, len(lines), 2)
]
# 绘制折线图
plt.figure(figsize=(12, 8))
for i, (harmonics, B_values) in enumerate(data_pairs):
    plt.plot(harmonics, B_values, label=string_names[i], marker='o')

# 添加图例、标签和标题
plt.legend(loc='upper right', title="String Types")
plt.xlabel('Harmonic Numbers')
plt.ylabel('B_values')
plt.title('Comparison of B_values Across Different Strings')
plt.grid(True)

# 保存图片到当前目录
plt.savefig('B_values_comparison.png', dpi=300)  # 高质量保存
print("图片已保存为 'B_values_comparison.png'")