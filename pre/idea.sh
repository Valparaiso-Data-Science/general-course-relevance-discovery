#!/bin/bash

file="ucat1920.xml" # change to $1

die(){
	echo $1 ; exit 1
}

id_desc_sep="</P><P>" # this separator will be replaced with a comma

[ -e "$file" ] || die "File '$file' doesn't exist"

#grep -E "^<P>[A-Z]{2,} [0-9]{2,}" $file # Course ID regex
#cmd currently requires gnu sed (wont work on bsd or macos ootb)
#the gnu-ism is now replaced (sed's -r option is now -E), so in theory it should work on POSIX systems
cat "$file" | tr -d '\n' | sed -E 's~(<P>[A-Z]{2,} [0-9]{2,})~\n\1~g'

# other commands I was investigating
#| sed 's/\(<P>[A-Z]{2,} [0-9]{2,}\)/\n\1/g'
#sed "s/<P>[A-Z]{2,} [0-9]{2,}/\n&/g"
#| sed 's/(<P>[A-Z]{2,} [0-9]{2,})/\n\\1/g'
#| perl -pe 's#(<P>[A-Z]{2,} )#\n$1#'
#| grep -e "^<P>[A-Z]{2,} [0-9]{2,}"
#| sed "s|$id_desc_sep|,|"
