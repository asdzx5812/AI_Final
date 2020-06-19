#! /usr/bin/env bash
for i in {1..11}; do
	echo "python Model.py -dir cmp_days -day 10 -f Prob_02_${i} --no-ani"
	python Model.py -dir cmp_days -day 10 -f Prob_02_${i} --no-ani
done

