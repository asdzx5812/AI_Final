#! /usr/bin/env bash
for i in {1..6}; do
	echo "python3 Model.py -day 10 -i $1 -dir cmp_infection -f i$1_${i} --no-ani"
	python3 Model.py -i $1 -d 10 -dir cmp_infection -f i$1_${i} --no-ani
done

