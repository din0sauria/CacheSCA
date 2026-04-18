import os
import sys
from gmssl import sm4

def random_bytes(size: int) -> bytes:
	return os.urandom(size)

def encrypt_sm4_block(plaintext: bytes, key: bytes) -> bytes:
	assert len(plaintext) == 16 and len(key) == 16, "Invalid plaintext or key size"

	cipher = sm4.CryptSM4()
	cipher.set_key(key, sm4.SM4_ENCRYPT)
	ciphertext = cipher.crypt_ecb(plaintext)

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
		ciphertext 	= encrypt_sm4_block(plaintext, key)
		samples.append((key, plaintext, ciphertext))
	
	with open(output_file, "w") as f:
		for key, plaintext, ciphertext in samples:
			f.write(f"{key.hex()} {plaintext.hex()} {ciphertext.hex()}\n")

	print(f"Generated {nsamples} SM4 samples in {output_file}")

if __name__ == "__main__":
	main()