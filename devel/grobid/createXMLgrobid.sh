#!/usr/bin/env sh

xml_out_dir="out" #obviously change

mkdir -pv $xml_out_dir

start_docker(){
	docker kill grobid # assumes container name is grobid
	docker run -d -t --rm --name grobid --init -p 8080:8070 -p 8081:8071 lfoppiano/grobid:0.6.0
}

copy_config(){
	cp config.json grobid-python-client/
}


python_client(){
	python3 grobid-python-client/grobid-client.py --input $in_dir --output $out_dir processFulltextDocument
}

