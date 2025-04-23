CC      = gcc
CFLAGS  = -O2 -std=c11 -pthread
LDFLAGS = -lm                  #  ←  math kütüphanesi
TARGET  = primemt

$(TARGET): primemt_20200808070.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	@> Results_20200808070.txt
	@for t in 1 2 4 8 16 32 64 128 256 512 1024 2048; do \
	  /usr/bin/time -f "Threads: $$t, Time taken: %e seconds" ./$(TARGET) $$t 2>> Results_20200808070.txt; \
	done

primemt_seg: primemt_seg_20200808070.c
	$(CC) $(CFLAGS) $< -o $@ -lm
