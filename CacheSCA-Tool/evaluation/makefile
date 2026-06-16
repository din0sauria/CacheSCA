HITLS_DIR = ../hitls
MASTIK_DIR = Mastik

CFLAGS = -Wall -Wextra -pedantic
LDFLAGS = -L$(HITLS_DIR) -L$(HITLS_DIR)/original/ -L$(MASTIK_DIR)/src/ -lboundscheck -lmastik -lhitls_crypto

aes: main.c wrapper.c wrapper.h $(HITLS_DIR)/declarations.h $(MASTIK_DIR)/src/libmastik.a
	$(CC) -o $@ $< wrapper.c $(LDFLAGS) $(CFLAGS) -DAES

sm4: main.c wrapper.c wrapper.h $(HITLS_DIR)/declarations.h $(MASTIK_DIR)/src/libmastik.a
	$(CC) -o $@ $< wrapper.c $(LDFLAGS) $(CFLAGS) -DSM4

$(MASTIK_DIR)/src/libmastik.a: $(MASTIK_DIR)/Makefile
	$(MAKE) -j -C $(MASTIK_DIR)

$(MASTIK_DIR)/Makefile:
	cd $(MASTIK_DIR) && ./configure

ARGS ?=

run-aes-%: aes
	@target=$* && subdir=$${target#aes-} && LD_LIBRARY_PATH=$(HITLS_DIR)/$$subdir:$$LD_LIBRARY_PATH ./aes $(ARGS)

run-sm4-%: sm4
	@target=$* && subdir=$${target#sm4-} && LD_LIBRARY_PATH=$(HITLS_DIR)/$$subdir:$$LD_LIBRARY_PATH ./sm4 $(ARGS)
