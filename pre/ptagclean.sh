#!/bin/sh

# This script was made mainly to combat Valpo's ugly XML

file=$1
# replace anything that has extra text in the ptag with '<p>'
# basically '<p lots_of_extra_stuff asdfasdfasdf >' --> '<p>'
sed "s|<p[^>]*>|<p>|" $file
