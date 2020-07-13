#!/usr/bin/env sh

xml_out_dir="out" #obviously change

#mkdir -pv $xml_out_dir

#csv_f=$1 # csv file is our input, we will download all of the pdfs in it and run them through grobid.

default_year="latest" #default year to download pdfs from
	# latest - uses makelatestcsv.sh to get the csv file
	# 15-16,16-17,etc - automate getpdfs to download the appropriate pdfs
	# all - use getpdfs download all function

check_environment(){
	docker --version || echo "Docker is not installed. Exiting..." && exit 1
	python --version || echo "Python is not installed. Exiting..." && exit 1
}

start_docker(){
	docker kill grobid # assumes container name is grobid
	docker run -d -t --rm --name grobid --init -p 8080:8070 -p 8081:8071 lfoppiano/grobid:0.6.0
}

copy_config(){
	cp config.json grobid-python-client/
}

python_client(){
	in_dir=$1
	out_idr=$2
	python3 grobid-python-client/grobid-client.py --input $in_dir --output $out_dir processFulltextDocument
}

down_pdfs(){
	year=$1
	cwd=$PWD
	cd "../fetchpdfs"
	case $year in
		latest)./makelatestcsv.sh && echo All | ./getpdfs.sh latest.csv;;
		All)echo All | ./getpdfs.sh;;
		*) echo $year | ./getpdfs.sh;;
	esac
	cd $cwd
}


# need to figure out how to decide which catalogs to download (use the scripts in fetchpdfs)




