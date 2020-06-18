#!/bin/sh

#valpo's catalog
file="../fullPDFs/ucat1920.xml"

# clean ptags
bash ptagclean.sh $file > 1
# p -> P
bash ptoPtag.sh 1 > 2
# remove b tags from doc
bash removeBtags 2 > 3
# run idea.sh (puts all things that look like a course ID on their own line)
bash idea.sh 3 > 4
# all actual courses have this regex sequence
grep '</P><P> </P><P>' 4 > 5
# remove the junk at the top of the xml
grep -v "<?xml" 5 > 6
# get rid of lines that have 10 or more periods in them (table of contents, etc)
grep -vE "\.{10}" 6 > 7
# print lines that are only 30 or more characters
grep -xE "^.{30,}$" 7 > 8
# print lines that have this regex sequence (could be moved to the earlier ('all actual courses...')
grep "Cr\. <\/P><P> <\/P><P>" 8 > 9
# divid the credits from the description
sed -E "s~Cr\. <\/P><P> <\/P><P>~Cr : ~" 9 > 10
# divide the course id from the title
sed -E "s~<\/P><P>~: ~" 10 > 11
# divide the title from the credits
sed -E "s~<\/P><P>~: ~" 11 > 12
# replace all ptags with nothing (re could be "<(\/|)P>")
sed -E "s~<\/P><P>~~g" 12 > 13

# remove all temporary files
rm 1 2 3 4 5 6 7 8 9 10 11 12
