#!/usr/bin/env sh

start_docker(){

	docker kill grobid # assumes container name is grobid
	docker run -d -t --rm --name grobid --init -p 8080:8070 -p 8081:8071 lfoppiano/grobid:0.6.0

}




