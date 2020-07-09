#!/usr/bin/env sh

f="urls.csv"

important_years="19-20 20-21"

grep -E "^(u|b)" $f > t

for y in $important_years
do
	grep $y t
done


schools=$(cut -d',' -f2 $f | sort | uniq)


mkdir -pv temp

for s in $schools
do
	grep $s urls.csv > temp/$s.csv
done



