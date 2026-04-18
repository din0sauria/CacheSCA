import os

def random_bytes(size: int) -> bytes:
	return os.urandom(size)

def primeprobe(target: str, cipher: str, key: bytes, filepath: str) -> None:
	os.system(f'make run-{cipher}-{target} ARGS="-k {key.hex()}" > {filepath}')

def test_key(target: str, cipher: str, key: bytes, root_dir: str) -> None:
	dir = '/'.join([root_dir, target, key.hex()])
	print(dir)
	os.makedirs(dir, exist_ok=True)

	for i in range(10):
		filepath = '/'.join([dir, f"trace_{i:02}"])
		primeprobe(target, cipher, key, filepath)

def test_target(target: str, cipher: str, root_dir: str) -> None:
	for i in range(10):
		key = random_bytes(16)
		test_key(target, cipher, key, root_dir)

def main() -> None:
	for target in ['original', 'aes_preload', 'aes_constant_time', 'aes_lut_p']:
		test_target(target, 'aes', 'traces/aes')

	for target in ['original', 'sm4_preload', 'sm4_lut_p']:
		test_target(target, 'sm4', 'traces/sm4')

if __name__ == "__main__":
	main()
