#!/usr/bin/env bash
THREADS=(1 2 4 8 16 32 64 128 256 512 1024 2048)

# Trial-division sonuçları
: > Results_20200808070.txt
for t in "${THREADS[@]}"; do
    echo "Trial: $t threads..."
    /usr/bin/time -f "Threads: $t, Time taken: %e seconds" ./primemt "$t" \
        2>> Results_20200808070.txt
done

# Segmented-sieve sonuçları
: > Results_seg_20200808070.txt
for t in "${THREADS[@]}"; do
    echo "Segmented: $t threads..."
    /usr/bin/time -f "Threads: $t, Time taken: %e seconds" ./primemt_seg "$t" \
        2>> Results_seg_20200808070.txt
done

echo "Tüm ölçümler tamamlandı."
