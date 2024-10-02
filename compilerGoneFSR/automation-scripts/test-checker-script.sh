#!/bin/bash
if ! [ -d ./solutions/checker-solutions ]; then
	mkdir solutions/checker-solutions
else 
	rm -r solutions/checker-solutions
	mkdir solutions/checker-solutions
fi
testDir=solutions/checker-solutions
file=$testDir/solution-checktest
for i in {0..7}
do
	echo "checktest$i" >> $file$i.txt
	echo "Solution >>>" >> $file$i.txt
	python3 -m goner.checker Tests/checktest$i.g &>>  $file$i.txt	
	echo "<<<<" >> $file$i.txt
	echo "My implementation solution" >> $file$i.txt
	python3 -m gone.checker Tests/checktest$i.g &>> $file$i.txt
done
