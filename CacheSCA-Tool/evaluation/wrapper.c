#include "wrapper.h"

#include "../hitls/declarations.h"

// Wrapper functions to match the mastik aes.h interface
void wp_set_encrypt_key128(void *rdkey, const uint8_t *key) {
#ifndef SM4
	SetEncryptKey128((CRYPT_AES_Key *)rdkey, key);
#else
	CRYPT_SM4_SetKey((CRYPT_SM4_Ctx *)rdkey, key, BLOCK_SIZE);
#endif
}

void wp_encrypt_block(uint8_t *input, uint8_t *output, void *rdkey) {
#ifndef SM4
	CRYPT_AES_Encrypt((const CRYPT_AES_Key *)rdkey, input, output, BLOCK_SIZE);
#else
	CRYPT_SM4_Encrypt((CRYPT_SM4_Ctx *)rdkey, input, output, BLOCK_SIZE);
#endif
}