import matplotlib.pyplot as plt
len_combs = [5, 6, 8, 8]
base = [2, 5, 7, 9]
single_time = [0.00007, 0.004, 0.9, 6.8]
parallel_time = [0.0005, 0.002, 0.3,  2.6]
python_time = [0.00003, 0.004, 0.85, 6.9]

plt.plot(base, single_time, label='(C) single thread', color='red')
plt.plot(base, parallel_time, label='(C) multi thread', color='blue')
plt.plot(base, python_time, label='(Python) itertools.product', color='green')

x_axis_labels = [f'{i}\n{j}' for i, j in zip(base, len_combs)]
plt.xticks(base, labels=x_axis_labels)
plt.xlabel('Base Number')
plt.ylabel('Exec Time')
plt.title('Programs Comparison')
plt.legend()
plt.savefig("plots/programs_comparison.png")
