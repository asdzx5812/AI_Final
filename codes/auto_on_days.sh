#! /usr/bin/env bash
for i in {1..11}; do
	echo "python Model.py -dir cmp_days -day $1 -f day_$1_${i} --no-ani"
	python Model.py -dir cmp_days -day $1 -f day_$1_${i} --no-ani
done

