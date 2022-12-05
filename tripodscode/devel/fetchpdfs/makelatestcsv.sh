#!/usr/bin/env sh

f="urls.csv" # shouldn't be changed

# searches for lines that start with one of: u, b, g
#	- get the second column
#		- use sort to get only 1 of each entry
schools=$(grep -E "^[ubg]" $f | cut -d',' -f2 | sort -u)

mkdir -pv temp

# for every school in the schools
for s in $schools
do
	# get valid lines of the school in the csv
	grep ",$s," urls.csv > temp/$s.csv
done

# for every file in the temp directory
for c in $(ls temp)
do
	# get rid of lines that start with 'g' (graduate catalogs)
	#	- then sort the lines in reverse numeric order (bigger to smaller; 9-1)
	# 		- then save that in a new file
	grep -v "^g" temp/$c | sort -nr > temp/$(echo $c | cut -d'.' -f1)_sorted.csv
	# remove the file
	rm temp/$c
done

# create the latest.csv file or, if it exists, empty it
> latest.csv
# for every spaced csv
for s_c in $(ls temp)
do
	# use sed to print the first line, thats what 'q' does
	sed q temp/$s_c >> latest.csv
done
# remove the 'temp' directory
rm -rf temp
