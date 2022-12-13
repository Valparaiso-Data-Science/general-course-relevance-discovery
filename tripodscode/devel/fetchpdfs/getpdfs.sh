#!/usr/bin/env sh


csv="${1:-urls.csv}"

echo "Valid Years:"
# get a valid list of years
years="$(cut -d',' -f3 $csv | sort -u | grep -vE "[a-z]") All"
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
	# if the input year matches one of the years in years,
	# then set valid_year to be true
	[ $target_year = $y ] && valid_year=0
done

# if valid year does not equal 0
! [ $valid_year -eq 0 ] && echo "Invalid input, exiting..." && exit 1

echo ""
echo "Downloading your PDFs for $target_year now..."

output_d="pdfs/"
# currently a bug with this line, works for numeric years, but not the 'All' option
urls=$(grep $target_year $csv | cut -d',' -f4)
# case statement should fix it
case $target_year in
	All) urls=$(cut -d',' -f4 $csv);;
	*) urls=$(grep $target_year $csv | cut -d',' -f4)
esac

# make the output directory and change into it
mkdir -pv $output_d && cd $output_d
for url in $urls
do

	file_name_string="$(grep $url "../$csv" | cut -d',' -f1-3 | tr ',' '_').pdf"
	# download the url via wget; silence the output; and concurrently
	wget $url -O "$file_name_string" 2>&1 1> /dev/null &
done
wait

echo "Your pdfs are now available in $output_d"
