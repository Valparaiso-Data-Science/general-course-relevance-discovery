#!/bin/sh

file="../fullPDFs/ucat1920.xml"



bash ptagclean.sh $file > 1

bash ptoPtag.sh 1 > 2

bash removeBtags 2 > 3

bash idea.sh 3 > 4

grep '</P><P> </P><P>' 4 > 5

grep -v "<?xml" 5 > 6

grep -vE "\.{10}" 6 > 7

grep -xE "^.{30,}$" 7 > 8

grep "Cr\. <\/P><P> <\/P><P>" 8 > 9

sed -E "s~Cr\. <\/P><P> <\/P><P>~Cr : ~" 9 > 10

sed -E "s~<\/P><P>~: ~" 10 > 11
sed -E "s~<\/P><P>~: ~" 11 > 12
sed -E "s~<\/P><P>~~g" 12 > 13


rm 1 2 3 4 5 6 7 8 9 10 11 12
