#! /usr/bin/env bash

old_q=`cat SEIR_Model.py | sed -n "10p"`
old_p=`cat SEIR_Model.py | sed -n "11p"`
old_m=`cat SEIR_Model.py | sed -n "12p"`

old_q=`echo $old_q`
old_p=`echo $old_p`
old_m=`echo $old_m`


new_p="MASK_PROTECTION_PROB = $1"
new_q="QUARANTINE_PROB = $2"
new_m="WEARING_MASK_PROB = $3"

#echo $new_p
#echo $new_q
#echo $new_m
cat SEIR_Model.py | sed "s/$old_q/$new_q/g" -i SEIR_Model.py
cat SEIR_Model.py | sed "s/$old_p/$new_p/g" -i SEIR_Model.py
cat SEIR_Model.py | sed "s/$old_m/$new_m/g" -i SEIR_Model.py


mkdir ../outputs/pr$1_q$2_w$3

for i in {1..5}; do
	echo "python Model.py -day 10 -n 3000 -i 1 -dir pr$1_q$2_w$3 -f $i --no-ani"
	python Model.py -day 10 -n 3000 -i 1 -dir pr$1_q$2_w$3 -f $i --no-ani &

	#python Model.py -day 10 -n 3000 -i 1 -dir $1 -f $i --no-ani &


	#echo "python3 Model.py -day 10 -i $1 -dir cmp_infection -f i${1}_${i} --no-ani"
	#python3 Model.py -day 10 -i $1 -dir cmp_infection -f i$1_${i} --no-ani
done
#'''
