f=$1

> temp_file

for t in $(cat bok.txt | tr ' ' '~')
do
	ns=$(echo $t | tr '~' ' ' | tr '[:upper:]' '[:lower:]' | tr -d '"')
	grep "$ns" $f >> temp_file
done

cat temp_file | sort | uniq > out
rm temp_file
