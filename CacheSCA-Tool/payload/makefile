TIMEOUT = 8
TARGET = main

.PHONY: low medium high extreme

low:
	cpulimit -l 100 -b -z -e $(TARGET)
	stress-ng --vm 4 --vm-bytes 1G --vm-hang $(TIMEOUT) --timeout $(TIMEOUT)

medium:
	cpulimit -l 50 -b -z -e $(TARGET)
	stress-ng --vm 4 --vm-bytes 2G --vm-hang $(TIMEOUT) --timeout $(TIMEOUT)

high:
	cpulimit -l 20 -b -z -e $(TARGET)
	stress-ng --vm 8 --vm-bytes 4G --vm-hang $(TIMEOUT) --timeout $(TIMEOUT)

extreme:
	cpulimit -l 10 -b -z -e $(TARGET)
	stress-ng --vm 16 --vm-bytes 8G --vm-hang $(TIMEOUT) --timeout $(TIMEOUT)
