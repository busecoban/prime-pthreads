#!/usr/bin/env bash
THREADS=(1 2 4 8 16 32 64 128 256 512 1024 2048)

: > Results_20200808070.txt
for t in "${THREADS[@]}"; do
    /usr/bin/time -f "Threads: $t, Time taken: %e seconds" ./primemt "$t" \
        2>> Results_20200808070.txt
done

