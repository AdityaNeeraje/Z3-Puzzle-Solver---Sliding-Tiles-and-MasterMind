#! /bin/bash

n=6
cols=4

total_tests=$((n**cols - 1))

for i in $(seq 0 $total_tests); do
    for j in $(seq 1 $cols); do
        echo -n $((i%n));
        echo -n " ";
        i=$((i/n));
    done | python3.10 ./mastermind.py
    # echo -ne "\n";
done

# python3.10 ./mastermind.py