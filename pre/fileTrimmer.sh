#!/bin/sh

#USAGE:
#
# sh fileTrimmer.sh <catalog>.csv <source_xml_directory>/ <output_directory>/
#

#DEPENDS:
#
#find, pwd, mkdir, echo, cut, sed
#
#Not tested with non-GNU tools

#Takes in a csv file and a directory as input
#The directory is where all of your XML files are (ie, orig/, sourceXMLs/, etc)
#The CSV file should be set up like below
#filenames are in column 1
#start line is in column 2
#end line is in column 3

#Anything before the start line is removed
#And Anything after the end line is removed

#WILL REMOVE ANY EMPTY XML FILES THAT ARE CREATED (ie in the $OUTPUT_DIR)
#
#Don't worry about any sed command errors, the script will still function just
#fine (Command errors are caused by cut not seeing any numbers in field 1 & 2
#for some of the lines)


ORIG_DIR=$(pwd) #reference point for 'removeEmptyFiles'
#OUTPUT_DIR='TRIMMED'

#CLI args (optargs would be better; need to refactor)
inputFile=$1
inputDir=$2
outputDir=$3

#Test the inputs, however this is not idiot proof, as the directory and the
#csv need to be in the right order for the script to function properly
[ -z $inputFile ] && echo "Need a CSV file to read!" && exit 1
[ -z $inputDir ] && echo "Need a directory path to where the XMLs are stored" && exit 1
[ -z $outputDir ] && echo "Using default directory '../temp_data/TRIMMED'!" && outputDir="../temp_data/TRIMMED"

OUTPUT_DIR="$outputDir"

mkdir -p "$OUTPUT_DIR"

fileNamesArr="$(cut -d',' -f1-3 < "$inputFile")"  #read in the first three fields of the catalog csv

for fileDesc in $fileNamesArr
do
	fileName=$(echo "$fileDesc" | cut -d',' -f1)
	startLine=$(echo "$fileDesc" | cut -d',' -f2)
	endLine=$(echo "$fileDesc" | cut -d',' -f3)
	#the sed command below just prints the stream from "startLine" to "endLine"
	#the -n is important as well, because if you didn't have it, sed would print out
	#the entire file and then apply the filters, and that is definitely not what you want
	sed -n "${startLine},${endLine}p" "$inputDir/$fileName.xml" > "$OUTPUT_DIR/${fileName}TRIMMED.xml" 2> /dev/null & #overwrites the file in the directory
done
wait

removeEmptyFiles(){
	cd $OUTPUT_DIR

	find $(pwd) -empty -type f -delete

	cd "$ORIG_DIR" #could be changed to 'cd ..' but it's not good to have relative paths in a shell script
}

removeEmptyFiles
