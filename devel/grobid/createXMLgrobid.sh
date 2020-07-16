#!/usr/bin/env sh

xml_out_dir="grobid_xmls" #obviously change

#mkdir -pv $xml_out_dir

#csv_f=$1 # csv file is our input, we will download all of the pdfs in it and run them through grobid.

default_year="latest" #default year to download pdfs from
	# latest - uses makelatestcsv.sh to get the csv file
	# 15-16,16-17,etc - automate getpdfs to download the appropriate pdfs
	# all - use getpdfs download all function

check_environment(){
	#docker --version || echo "Docker is not installed. Exiting..." && exit 1
	# this is commented out, because 'technically' you don't need docker installed
	# on the local computer
	python --version || echo "Python is not installed. Exiting..." && exit 1
}

start_docker(){
	docker kill grobid # assumes container name is grobid
	docker run -d -t --rm --name grobid --init -p 8080:8070 -p 8081:8071 lfoppiano/grobid:0.6.0
}

copy_config(){
	cp config.json grobid-client-python/
}

python_client(){
	in_dir=$1
	out_idr=$2
	python3 grobid-client-python/grobid-client.py --input $in_dir processFulltextDocument
}

down_pdfs(){
	# wrapper for ../getpdfs.sh
	year=$1
	cwd=$PWD
	d_s="../fetchpdfs"
	cd "../fetchpdfs"
	case $year in
		latest)./makelatestcsv.sh && echo All | ./getpdfs.sh latest.csv;;
		All)echo All | ./getpdfs.sh;;
		*) echo $year | ./getpdfs.sh;;
	esac
	cd $cwd
	[ -d pdfs ] && rm -rf pdfs
	mv -f "${d_s}/pdfs/" .
}

# this is the method that I would need to change
rand_s(){
	#https://gist.github.com/earthgecko/3089509
	# it works by getting random strings from /dev/urandom
	# then using 'tr' it gets rid of anything that isn't alphanumeric
	# it then folds each line to only be 10 characters long
	# then it prints out the first line
	cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | sed q
}

sep_pdfs(){
	# separate every pdf in 'pdfs/' into its own directory
	cwd=$PWD
	[ -d sep ] && rm -rf sep
	mkdir sep && cd sep
	for pdf in $(ls ../pdfs/ | tr ' ' '~')
	do
		r_s=$(rand_s)
		mkdir -v $r_s && cp "../pdfs/$(echo $pdf | tr '~' ' ')" $r_s
	done

	cd $cwd
}


main(){
	#check_environment
	#start_docker
	#copy_config
	down_pdfs $default_year
	sep_pdfs

	for d in $(ls sep/)
	do
		python_client "sep/$d"
	done

	xml_files=$(find sep -type f | grep xml)
	for xml in xml_files
	do
		cp $xml $xml_out_dir
	done
	echo "XML files should now be in $xml_out_dir"
}

main

