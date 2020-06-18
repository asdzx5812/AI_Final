#! /usr/bin/env bash
for i in {1..11}; do
	echo "python Model.py -i $1 -d 15 -f i$1_${i} --no-ani"
	python Model.py -i $1 -d 15 -f i$1_${i} --no-ani
done

