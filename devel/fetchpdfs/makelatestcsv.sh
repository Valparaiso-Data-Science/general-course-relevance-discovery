#!/usr/bin/env sh

f="urls.csv"

schools=$(grep -E "^[ubg]" $f | cut -d',' -f2 | sort -u)

mkdir -pv temp

for s in $schools
do
	grep ",$s," urls.csv > temp/$s.csv
done

for c in $(ls temp)
do
	grep -v "^g" temp/$c | sort -nr > temp/$(echo $c | cut -d'.' -f1)_sorted.csv
	rm temp/$c
done

> latest.csv
for s_c in $(ls temp)
do
	sed q temp/$s_c >> latest.csv
done

rm -rf temp
