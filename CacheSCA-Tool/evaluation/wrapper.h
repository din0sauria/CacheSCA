#include <stdint.h>
#include <stddef.h>

#define BLOCK_SIZE 16

void wp_set_encrypt_key128(void *rdkey, const uint8_t *key);
void wp_encrypt_block(uint8_t *input, uint8_t *output, void *rdkey);
