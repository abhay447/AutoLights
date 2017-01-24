#! /bin/bash
for i in `seq 1 100`;do
    echo "Training Run: "$i
    python -W ignore rl.py -m train
done
