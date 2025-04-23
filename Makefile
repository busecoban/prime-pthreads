CC      = gcc
CFLAGS  = -O2 -std=c11 -pthread
LDFLAGS = -lm                  #  ←  math kütüphanesi
TARGET  = primemt

$(TARGET): primemt_20200808070.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)


primemt_seg: primemt_seg_20200808070.c
	$(CC) $(CFLAGS) $< -o $@ -lm
