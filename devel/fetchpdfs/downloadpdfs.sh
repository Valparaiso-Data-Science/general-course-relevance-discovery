#!/usr/bin/env sh

csv_f=$1 #csv file
years="$2"
out_d="${3:-pdfs}" #output directory

[ -z $csv_f ] && echo "Missing CSV file. Exiting..." && exit 1
[ -z $years ] && echo "No years were given. Exiting..." && exit 1
mkdir -p $out_d && cd $out_d # make the output directory and change into it

case $years in
	All) urls_s=$(cut -d',' -f4 $csv_f);;
	*) urls_s=$(grep $years $csv_f | cut -d',' -f4)
esac

for url in $urls_s # for all of the urls
do
	wget "$url" & # download the pdf (concurrently)
done
wait # wait for all of the downloads to finish
