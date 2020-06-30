#!/usr/bin/env sh

csv_f=$1
out_d="${2:-out}"

[ -z $csv_f ] && echo "Missing CSV file. Exiting..." && exit 1

mkdir -p $out_d && cd $out_d # make the output directory and change into it

for url in $(cat $1 | cut -d',' -f4) # looks specifically at the fourth element of the csv
do
	wget "$url" & # download the pdf (concurrently)
done
wait # wait for all of the downloads to finish
