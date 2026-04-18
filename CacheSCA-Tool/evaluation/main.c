#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>

#include <mastik/util.h>
#include <mastik/synctrace.h>

#include "../hitls/declarations.h"
#include "wrapper.h"

#define NSAMPLES	100000

void usage(const char *p);
void str2bytes(const char *str, uint8_t *bytes, size_t len);
uint8_t clusterMask(uint8_t input[], int byte);

int main(int argc, char **argv) {
	int samples = NSAMPLES;
	char *keystr = "0b7e151628aed2a6abf7158809cf4f3c";

	int ch;
	while ((ch = getopt(argc, argv, "s:k:")) != -1) {
		switch (ch) {
			case 's':
				samples = atoi(optarg);
				break;
			case 'k':
				keystr = optarg;
				break;

			default:
				usage(argv[0]);
		}
	}

	uint8_t key[16];
	str2bytes(keystr, key, sizeof(key));

#ifndef SM4
	CRYPT_AES_Key skey;
#else
	CRYPT_SM4_Ctx skey;
#endif
	wp_set_encrypt_key128((void*)&skey, key);

#ifdef SM4
	for (int i = 0; i < CRYPT_SM4_ROUNDS; ++i) {
		printf("RK[%2d] = %08X\n", i, skey.rk[i]);
	}
#endif

	delayloop(1000000000);

	st_clusters_t clusters = syncPrimeProbe(
		samples,
		BLOCK_SIZE,
		1,
		NULL,
		NULL,
		wp_encrypt_block,
		(void*)&skey,
		clusterMask,
		1
	);

	for (int i = 0; i < 16; ++i) {
		for (int pt = 0; pt < 256; ++pt) {
			if (clusters[i].count[pt] == 0)
				continue;
			
			printf("%d %02X: ", i, pt);
			for (int off = 0; off < L1_SETS; ++off) {
				printf("%ld ", clusters[i].avg[pt][off]);
			}
			puts("");
		}
	}
	
	free(clusters);

	return 0;
}

void usage(const char *p) {
	fprintf(stderr, "Usage: %s [-s <samples>]\n", p);
	exit(1);
}

void str2bytes(const char *str, uint8_t *bytes, size_t len) {
	for (size_t i = 0; i < len; ++i) {
		sscanf(str + 2 * i, "%2hhx", &bytes[i]);
	}
}


#define GET_UINT32_BE(p, i)                  \
(                                            \
    ((uint32_t)(p)[(i) + 0] << 24) |         \
    ((uint32_t)(p)[(i) + 1] << 16) |         \
    ((uint32_t)(p)[(i) + 2] <<  8) |         \
    ((uint32_t)(p)[(i) + 3] <<  0)           \
)

uint8_t clusterMask(uint8_t input[], int byte) {
#ifndef SM4
	return input[byte] & 0xF0;
#else
	// uint32_t X0 = GET_UINT32_BE(input, 0);
	uint32_t X1 = GET_UINT32_BE(input, 4);
	uint32_t X2 = GET_UINT32_BE(input, 8);
	uint32_t X3 = GET_UINT32_BE(input, 12);

	uint32_t tmp = X1 ^ X2 ^ X3;
	int shift = (3 - byte % 4) * 8;

	return (tmp >> shift) & 0xF0;
#endif
}
