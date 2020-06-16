#!/bin/sh

# This script was made mainly to combat Valpo's ugly XML

file=$1
sed "s|<p[^>]*>|<p>|" $file
