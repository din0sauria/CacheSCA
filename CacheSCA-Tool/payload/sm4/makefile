HITLS_DIR = ../../hitls

CFLAGS = -O2 -Wall -Wextra -pedantic
LDFLAGS = -L$(HITLS_DIR) -L$(HITLS_DIR)/original -lboundscheck -lhitls_crypto

main: main.c $(HITLS_DIR)/declarations.h
	$(CC) -o $@ $< $(LDFLAGS) $(CFLAGS)

run-%: main $(HITLS_DIR)/%/libhitls_crypto.so
	@LD_LIBRARY_PATH=$(HITLS_DIR)/$*/:"$LD_LIBRARY_PATH" ./main $(filter-out $@,$(MAKECMDGOALS))

%:
	@
