import matplotlib.pyplot as plt

file_sizes = [196, 434, 1086, 1536]
str_sizes = [153429, 555486, 2858320, 4705124]
nlfsr_sizes = [4307, 13825, 61827, 96552 ]

plt.plot(file_sizes, str_sizes, label='str format', color='red')
plt.plot(file_sizes, nlfsr_sizes, label='nlfsr format', color='blue')
plt.xlabel('File Sizes')
plt.ylabel('Format Sizes')
plt.title('Format Comparison')
plt.legend()
plt.savefig("plots/format_comparison.png")
