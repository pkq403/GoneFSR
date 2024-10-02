#!/bin/bash
benchmarkData="./coders_benchmark_data"

for file in "$benchmarkData"/*; do
        basenameFile=$(basename $file)
        echo "Coding: $basenameFile"
        echo "${basenameFile%.*}"
        python3 file_coder.py $file "./coded_benchmark_data/${basenameFile%.*}.bin"
done

