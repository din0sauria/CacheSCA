import os
import sys
from Crypto.Cipher import AES

def random_bytes(size: int) -> bytes:
	return os.urandom(size)

def encrypt_aes_block(plaintext: bytes, key: bytes) -> bytes:
	assert len(plaintext) == 16 and len(key) in (16, 24, 32), "Invalid plaintext or key size"
	
	cipher = AES.new(key, AES.MODE_ECB)
	ciphertext = cipher.encrypt(plaintext)

	return ciphertext

def main() -> None:
	if len(sys.argv) != 3:
		print(f"Usage: {sys.argv[0]} <nsamples> <output_file>")
		return

	nsamples = int(sys.argv[1])
	output_file = sys.argv[2]

	samples = []
	for _ in range(nsamples):
		key 		= random_bytes(16)
		plaintext 	= random_bytes(16)
		ciphertext 	= encrypt_aes_block(plaintext, key)
		samples.append((key, plaintext, ciphertext))
	
	with open(output_file, "w") as f:
		for key, plaintext, ciphertext in samples:
			f.write(f"{key.hex()} {plaintext.hex()} {ciphertext.hex()}\n")

	print(f"Generated {nsamples} AES samples in {output_file}")

if __name__ == "__main__":
	main()