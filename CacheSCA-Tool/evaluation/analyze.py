import sys
import numpy as np
import pandas as pd

def heatmap(data: np.ndarray, rows: list, set_idx: np.ndarray) -> None:
	import matplotlib.pyplot as plt
	import seaborn as sns

	rows_str = [f'0x{r:02X}' for r in rows]
	df = pd.DataFrame(data[rows], index=rows_str)

	rank_df = df.rank(axis=1, ascending=False, method='dense').astype(int)

	annot_matrix = np.full(df.shape, "", dtype=object)
	for i in range(len(df)):
		for j in range(len(df.columns)):
			rk = rank_df.iloc[i, j]
			
			if rk < 10:
				annot_matrix[i, j] = f'{rk}'
			
			if j == set_idx[rows[i]]:
				annot_matrix[i, j] += '*'

	sns.heatmap(df, annot=annot_matrix, fmt="", cmap="viridis", cbar=True)

	plt.xlabel("Cache Set Index")
	plt.ylabel("Plaintext Byte Value")
	plt.title("Cache Access Heatmap")
	plt.show()

def analyze(data: np.ndarray, rows: list) -> None:
	maxn = -np.inf
	keybyte = -1
	offset = -1

	for guess in range(16):
		for off in range(64):
			sum = 0
			for pt in rows:
				set_idx = (off + ((pt >> 4) ^ guess)) % 64
				sum += data[pt, set_idx]

			if sum > maxn:
				maxn = sum
				keybyte = guess
				offset = off
	
	set_idx = np.zeros(256, dtype=int)
	for pt in rows:
		set_idx[pt] = (offset + ((pt >> 4) ^ keybyte)) % 64
	
	return keybyte << 4, offset, set_idx, maxn

def main():
	if len(sys.argv) != 2:
		print(f"Usage: {sys.argv[0]} <input_file>")
		return

	input_file = sys.argv[1]

	raw_data = np.zeros((16, 256, 64), dtype=int)
	valid_rows = []

	with open(input_file, "r") as f:
		for line in f:
			parts = line.strip().split(": ")
			if len(parts) != 2:
				continue

			try:
				idx, pt = parts[0].split()
				idx = int(idx)
				pt = int(pt, 16)
			except:
				continue

			values = list(map(int, parts[1].split()))

			raw_data[idx, pt] = np.array(values)

			if idx == 0:
				valid_rows.append(pt)

	for i in range(16):
		keybyte, _, set_idx, _ = analyze(raw_data[i], valid_rows)
		
		print(f"Byte {i:2}: {keybyte:02X}")

		heatmap(raw_data[i], valid_rows, set_idx)

if __name__ == "__main__":
	main()
