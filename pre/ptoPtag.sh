#!/bin/sh

file=$1
cat "$file" | sed 's|p>|P>|g' #only have to do the back half
