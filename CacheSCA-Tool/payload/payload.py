import multiprocessing
import subprocess
import sys
import time

def run_command(cmd, cwd, delay):
	"""执行命令并返回结果"""
	time.sleep(delay)
	try:
		result = subprocess.check_output(cmd, cwd=cwd, shell=True, text=True, stderr=subprocess.STDOUT)
		return result
	except subprocess.CalledProcessError as e:
		return f"Error: {e.output}"

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print("Usage: python payload.py <aim> <cipher> <datafile> <level>")
		sys.exit(1)

	aim = sys.argv[1]
	cipher = sys.argv[2].lower()
	datafile = sys.argv[3]
	level = sys.argv[4]

	commands = [
		(f"make run-{aim} {datafile} 0 2", cipher, 0),
		(f"make {level}", ".", 1)
	]
	
	# 使用进程池并行执行
	with multiprocessing.Pool() as pool:
		results = pool.starmap(run_command, commands)
	
	# # 打印结果
	for i, result in enumerate(results):
		print(f"Command {i+1} output:\n{result}")
	
	idx = results[0].find(' clock ticks')
	if idx < 0:
		print("0")
	else:
		start_idx = results[0].rfind(' ', 0, idx) + 1
		print(results[0][start_idx:idx])