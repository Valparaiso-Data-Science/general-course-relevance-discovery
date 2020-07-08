#!/usr/bin/env sh

help(){
	echo ""
}


echo "Valid Years:"
years="$(cat urls.csv | cut -d',' -f3 | sort | uniq | grep -vE "[a-z]") All"
for y in $years
do
	case $y in
		All) n_c="$(wc -l urls.csv)";;
		*) n_c="$(grep $y urls.csv | wc -l)";;
	esac
	echo "$y N: $n_c"
done

printf "What year of catalogs would you like to download? "
read target_year

valid_year=1 # 1 for incorrect

for y in $years
do
	[ $target_year = $y ] && valid_year=0
done

# if valid year does not equal 0
! [ $valid_year -eq 0 ] && echo "Invalid input, exiting..." && exit 1

echo "Downloading your PDFs now..."

./downloadpdfs.sh "urls.csv" $valid_year

