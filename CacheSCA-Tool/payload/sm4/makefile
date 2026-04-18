CFLAGS = -O2 -Wall -Wextra -pedantic -lboundscheck
HITLS_DIR = ../../hitls

main: main.c $(HITLS_DIR)/declarations.h $(HITLS_DIR)/origin/libhitls_crypto.so
	$(CC) -o $@ $< -L$(HITLS_DIR)/original/ -lhitls_crypto $(CFLAGS)

run-%: main $(HITLS_DIR)/%/libhitls_crypto.so
	@LD_LIBRARY_PATH=$(HITLS_DIR)/$*/:"$LD_LIBRARY_PATH" ./main $(filter-out $@,$(MAKECMDGOALS))

%:
	@