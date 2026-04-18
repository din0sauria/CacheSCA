#include <stdint.h>
#include <stddef.h>

// =================== AES =================
#define CRYPT_AES_MAX_ROUNDS  14
#define CRYPT_AES_MAX_KEYLEN  (4 * (CRYPT_AES_MAX_ROUNDS + 1))

typedef struct {
    uint32_t key[CRYPT_AES_MAX_KEYLEN];
    uint32_t rounds;
} CRYPT_AES_Key;

void SetEncryptKey128(CRYPT_AES_Key *ctx, const uint8_t *key);
// void SetEncryptKey192(CRYPT_AES_Key *ctx, const uint8_t *key);
// void SetEncryptKey256(CRYPT_AES_Key *ctx, const uint8_t *key);
void SetDecryptKey128(CRYPT_AES_Key *ctx, const uint8_t *key);
// void SetDecryptKey192(CRYPT_AES_Key *ctx, const uint8_t *key);
// void SetDecryptKey256(CRYPT_AES_Key *ctx, const uint8_t *key);
int32_t CRYPT_AES_Encrypt(const CRYPT_AES_Key *ctx, const uint8_t *in, uint8_t *out, uint32_t len);
int32_t CRYPT_AES_Decrypt(const CRYPT_AES_Key *ctx, const uint8_t *in, uint8_t *out, uint32_t len);

// =================== SM4 =================
#define CRYPT_SM4_BLOCKSIZE     16
#define CRYPT_SM4_BLOCKSIZE_16  256
#define CRYPT_SM4_ROUNDS		32

typedef struct {
    uint8_t iv[CRYPT_SM4_BLOCKSIZE];
    uint32_t rk[CRYPT_SM4_ROUNDS];
} CRYPT_SM4_Ctx;

int32_t CRYPT_SM4_SetKey(CRYPT_SM4_Ctx *ctx, const uint8_t *key, uint32_t keyLen);
int32_t CRYPT_SM4_Encrypt(CRYPT_SM4_Ctx *ctx, const uint8_t *in, uint8_t *out, uint32_t length);
int32_t CRYPT_SM4_Decrypt(CRYPT_SM4_Ctx *ctx, const uint8_t *in, uint8_t *out, uint32_t length);
