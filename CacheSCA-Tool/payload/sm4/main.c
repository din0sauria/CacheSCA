#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

#include "../../hitls/declarations.h"

#define min(a, b) ((a) < (b) ? (a) : (b))

#ifndef BACKOFF_TIME_S
#define BACKOFF_TIME_S 3
#endif

#define NSAMPLES_MAX 100000

typedef struct {
	const char *input_file;
	const int	nsamples;
	const int	mode;
} config_t;

typedef uint8_t sm4_key_t[16];
typedef uint8_t sm4_block_t[16];

typedef struct {
	sm4_key_t	key;
	sm4_block_t	plaintext;
	sm4_block_t	ciphertext;
} sm4_sample_t;

void delay_s(unsigned int seconds);
config_t parse_args(int argc, char *argv[]);
int load_data(const config_t *config, sm4_sample_t samples[]);
void test_mode_0(const sm4_sample_t *samples, int nsamples);
void test_mode_1(const sm4_sample_t *samples, int nsamples);
void test_mode_2(const sm4_sample_t *samples, int nsamples);
bool block_equal(const sm4_block_t a, const sm4_block_t b);
void str2hex(const char *str, uint8_t *out, size_t out_len);
static inline clock_t timing(void);

int main(int argc, char *argv[]) {
	const config_t config = parse_args(argc, argv);

	sm4_sample_t samples[config.nsamples];
	int real_nsamples = load_data(&config, samples);

#ifdef DEBUG
	puts("Loaded samples:");	
	for (int i = 0; i < config.nsamples; ++i) {
		printf("Sample %d:\n", i);
		printf("  Key:       ");
		for (int j = 0; j < 16; ++j) printf("%02x", samples[i].key[j]);
		printf("\n  Plaintext: ");
		for (int j = 0; j < 16; ++j) printf("%02x", samples[i].plaintext[j]);
		printf("\n  Ciphertext:");
		for (int j = 0; j < 16; ++j) printf("%02x", samples[i].ciphertext[j]);
		printf("\n");
	}
#endif

	delay_s(BACKOFF_TIME_S);
	puts("Starting SM4 tests...");

	switch (config.mode) {
		case 0:
			test_mode_0(samples, real_nsamples);
			break;
		case 1:
			test_mode_1(samples, real_nsamples);
			break;
		case 2:
			test_mode_2(samples, real_nsamples);
			break;
		default:
			fprintf(stderr, "Invalid mode: %d\n", config.mode);
			return EXIT_FAILURE;
	}

	return 0;
}

void delay_s(unsigned int seconds) {
	time_t start = time(NULL);
	while (time(NULL) - start < seconds) {
		__asm__ volatile("nop");
	}
}

config_t parse_args(int argc, char *argv[]) {
	if (argc < 4) {
		fprintf(stderr, "Usage: %s <input_file> <nsamples> <mode>\n", argv[0]);
		exit(EXIT_FAILURE);
	}

	return (config_t){
		.input_file = argv[1],
		.nsamples	= atoi(argv[2]) ? min(atoi(argv[2]), NSAMPLES_MAX) : NSAMPLES_MAX,
		.mode		= atoi(argv[3]),
	};
}

int load_data(const config_t *config, sm4_sample_t samples[]) {
	FILE *fin = fopen(config->input_file, "r");
	if (!fin) {
		perror("Failed to open input file");
		exit(EXIT_FAILURE);
	}

	int real_nsamples = 0;
	char buffer[256];
	for (int i = 0; i < config->nsamples; ++i) {
		if (!fgets(buffer, sizeof(buffer), fin)) {
			real_nsamples = i;
			break;
		}

		char key_str[33], pt_str[33], ct_str[33];
		if (sscanf(buffer, "%32s %32s %32s", key_str, pt_str, ct_str) != 3) {
			break;
		}
		key_str[32] = pt_str[32] = ct_str[32] = '\0';
		str2hex(key_str, samples[i].key, 16);
		str2hex(pt_str, samples[i].plaintext, 16);
		str2hex(ct_str, samples[i].ciphertext, 16);
	}
	fclose(fin);

	return real_nsamples;
}

void test_mode_0(const sm4_sample_t *samples, int nsamples) {
	CRYPT_SM4_Ctx ctx;
	sm4_block_t out;

	puts("Testing SM4 Encryption...");

	(void)timing();
	for (int i = 0; i < nsamples; ++i) {
		CRYPT_SM4_SetKey(&ctx, samples[i].key, sizeof(sm4_key_t));
		CRYPT_SM4_Encrypt(&ctx, samples[i].plaintext, out, sizeof(sm4_block_t));

		if (!block_equal(out, samples[i].ciphertext)) {
			printf("Sample %d: Encryption mismatch!\n", i);
		}
	}
	clock_t enc_time = timing();
	printf("Encryption time for %d samples: %ld clock ticks\n", nsamples, enc_time);

	puts("Testing SM4 Decryption...");

	(void)timing();
	for (int i = 0; i < nsamples; ++i) {
		CRYPT_SM4_SetKey(&ctx, samples[i].key, sizeof(sm4_key_t));
		CRYPT_SM4_Decrypt(&ctx, samples[i].ciphertext, out, sizeof(sm4_block_t));

		if (!block_equal(out, samples[i].plaintext)) {
			printf("Sample %d: Decryption mismatch!\n", i);
		}
	}
	clock_t dec_time = timing();
	printf("Decryption time for %d samples: %ld clock ticks\n", nsamples, dec_time);

	puts("Tests completed.");
}

void test_mode_1(const sm4_sample_t *samples, int nsamples) {
	CRYPT_SM4_Ctx ctx;

	puts("Testing SM4 Key Expansion...");

	(void)timing();
	for (int i = 0; i < nsamples; ++i) {
		CRYPT_SM4_SetKey(&ctx, samples[i].key, sizeof(sm4_key_t));
	}
	clock_t enc_time = timing();
	printf("Key expansion time for %d samples: %ld clock ticks\n", nsamples, enc_time);

	puts("Tests completed.");
}

void test_mode_2(const sm4_sample_t *samples, int nsamples) {
	CRYPT_SM4_Ctx ctx;
	sm4_block_t out;

	puts("Testing SM4 Repeated Encryption...");

	(void)timing();
	CRYPT_SM4_SetKey(&ctx, samples[0].key, sizeof(sm4_key_t));
	for (int i = 0; i < nsamples; ++i) {
		CRYPT_SM4_Encrypt(&ctx, samples[i].plaintext, out, sizeof(sm4_block_t));
	}
	clock_t enc_time = timing();
	printf("Repeated encryption time for %d samples: %ld clock ticks\n", nsamples, enc_time);

	puts("Testing SM4 Repeated Decryption...");

	(void)timing();
	CRYPT_SM4_SetKey(&ctx, samples[0].key, sizeof(sm4_key_t));
	for (int i = 0; i < nsamples; ++i) {
		CRYPT_SM4_Decrypt(&ctx, samples[i].ciphertext, out, sizeof(sm4_block_t));
	}
	clock_t dec_time = timing();
	printf("Repeated decryption time for %d samples: %ld clock ticks\n", nsamples, dec_time);

	puts("Tests completed.");
}

bool block_equal(const sm4_block_t a, const sm4_block_t b) {
	return memcmp(a, b, sizeof(sm4_block_t)) == 0;
}

void str2hex(const char *str, uint8_t *out, size_t out_len) {
	for (size_t i = 0; i < out_len; ++i) {
		sscanf(&str[i * 2], "%2hhx", &out[i]);
	}
}
static inline clock_t timing(void) {
	static clock_t last = 0;
	clock_t now = clock();
	clock_t elapsed = now - last;
	last = now;
	return elapsed;
}
