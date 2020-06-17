#!/bin/sh

file=$1
sed 's|p>|P>|g' $file #only have to do the back half
