#!/bin/sh

#valpo's catalog
#file="fullPDFs/ucat1920.xml"
file=$1
out_d=$2
# clean ptags
#bash ptagclean.sh $file > 1
# replace anything that has extra text in the ptag with '<p>'
# basically '<p lots_of_extra_stuff asdfasdfasdf >' --> '<p>'
sed "s|<p[^>]*>|<p>|" $file > 1
# p -> P
#bash ptoPtag.sh 1 > 2
sed 's|p>|P>|g' 1 > 2 #only have to do the back half
# remove b tags from doc
#bash removeBtags 2 > 3
sed -E "s~<(/|)b>~~g" 2 > 3
# run idea.sh (puts all things that look like a course ID on their own line)
#bash idea.sh 3 > 4
cat 3 | tr -d '\n' | sed -E 's~(<P>[A-Z]{2,} [0-9]{2,})~\n\1~g' > 4
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
sed -E "s~Cr\. <\/P><P> <\/P><P>~Cr # ~" 9 > 10
# divide the course id from the title
sed -E "s~<\/P><P>~# ~" 10 > 11
# divide the title from the credits
sed -E "s~<\/P><P>~# ~" 11 > 12
# replace all ptags with nothing (re could be "<(\/|)P>")
sed -E "s~<\/P><P>~~g" 12 > 13
# get rid of all text after the closing ptag
sed -E "s~<\/P>.*$~~" 13 > 14
# get rid of lines that are 'course id # credits'
grep -vE "<P>[A-Z]{2,} [0-9]{2,} \# [0-9] Cr" 14 > 15
# get rid of lines that have a list of course id's
grep -vE "^<P>([A-Z]{2,} [0-9]{2,}, ){1,}" 15 > 16
# remove p tag at the beginning of the line
sed "s~^<P>~~" 16 > 17
# remove a tags
sed -E "s|<\/?a[^>]*>||g" 17 > 18
# delete all text between two i tags
sed -E "s~<i>.*[^(<\/i>)]<\/i>~~g" 18 > 19
# remove honors work courses (they all reference page 62)
grep -v "page 62" 19 > 20
# add quotes around all text fields
sed -E -e "s/^/\"/" -e "s~#~\"#\"~g" -e "s/$/\"/" 20 > 21
# now work on making it like the other schools
sed -e "s/#//" -e  "s/#//" -e "s/\"\"//g" 21 > 22 # get rid of the first two separators
sed -e "s/#/,/" -e "s/ , /,/" 22  > 23 # split course id from description
# add valpo's name; also final cleanup of 'weird' quotation marks
#sed -E -e "s~^~Valpo,~" -e "s~&\"#\"34;~'~g" -e "s~(\ ){1,}~ ~g" 23 > 24
sed -E -e "s~^~,Valpo,~" -e "s~&\"#\"34;~'~g" -e "s~(\ ){1,}~ ~g" 23 > 24
#nl 24 | sed "s/ //" > 25
#echo "School,CourseID,Descriptions" >> "$out_d/valpo.csv"
cat 24 >> "$out_d/valpo.csv"

# remove all temporary files

# if you want to remove double spaces '  '
# you can run this sed command: sed -E "s~(\ ){1,}~ ~g"

# the only bugs that I am currently aware of is that there are a few non courses that
# get added in, and some classes are missing the last few words (things like prereqs and
# what not)

# the script should be in a usable state now though

for i in $(seq 24)
do
	rm $i
done

# &"#"34;



