#!/bin/bash
# the argument given to this script
file="$1"

# echoes the argument fed to it and exits with an error (1)
die(){
	echo $1 ; exit 1
}
# test if the file exists, and if not, die
[ -e "$file" ] || die "File '$file' doesn't exist"

#grep -E "^<P>[A-Z]{2,} [0-9]{2,}" $file # Course ID regex
#cmd currently requires gnu sed (wont work on bsd or macos ootb)
#the gnu-ism is now replaced (sed's -r option is now -E), so in theory it should work on POSIX systems

# get the files contents (via cat) and pipe it into tr, deleting all of the newlines
# then pipe the output from that command into sed
# the sed command searches for an open p tag and course ID and puts it on a newline
# with the regex match that it found (so that it is not removed)
cat "$file" | tr -d '\n' | sed -E 's~(<P>[A-Z]{2,} [0-9]{2,})~\n\1~g'

# other commands I was investigating
#| sed 's/\(<P>[A-Z]{2,} [0-9]{2,}\)/\n\1/g'
#| sed "s/<P>[A-Z]{2,} [0-9]{2,}/\n&/g"
#| sed 's/(<P>[A-Z]{2,} [0-9]{2,})/\n\\1/g'
#| perl -pe 's#(<P>[A-Z]{2,} )#\n$1#'
#| grep -e "^<P>[A-Z]{2,} [0-9]{2,}"
#| sed "s|$id_desc_sep|,|"
