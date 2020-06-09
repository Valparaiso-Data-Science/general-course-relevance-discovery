#!/bin/sh
file=$1
cat $1 | sed "s|<p[^>]*>|<p>|"
