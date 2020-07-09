#!/usr/bin/env sh

help(){
	echo ""
}

csv="urls.csv"

echo "Valid Years:"
years="$(cut -d',' -f3 $csv | sort | uniq | grep -vE "[a-z]") All"
for y in $years
do
	case $y in
		All) n_c="$(wc -l $csv)";;
		*) n_c="$(grep $y $csv | wc -l)";;
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

echo ""
echo "Downloading your PDFs for $target_year now..."
#echo $target_year

#sh downloadpdfs.sh $csv $target_year

output_d="pdfs/"

urls=$(grep $target_year $csv | cut -d',' -f4)

mkdir -pv $output_d && cd $output_d
for url in $urls
do
	wget $url 2>&1 1> /dev/null &
done
wait

echo "Your pdfs are now available in $output_d"
