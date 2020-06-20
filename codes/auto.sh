#! /usr/bin/env bash
for i in {1..11}; do
	if [[ $i -eq 1 ]]; then
		echo "python Model.py -dir cmp_days -day 10 -f Prob_02_${i}"
		python Model.py -dir cmp_days -day 10 -f Prob_02_${i}
	else
		echo "python Model.py -dir cmp_days -day 10 -f Prob_02_${i} --no-ani"
		python Model.py -dir cmp_days -day 10 -f Prob_02_${i} --no-ani
	fi
done

