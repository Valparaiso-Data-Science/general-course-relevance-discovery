#!/bin/sh

file=$1
# capitalizes the p in a ptag
sed 's|p>|P>|g' $file #only have to do the back half
