#!/bin/bash
if ! [ -d ./solutions/ircode-solutions ]; then
	mkdir solutions/ircode-solutions
else 
	rm -r solutions/ircode-solutions
	mkdir solutions/ircode-solutions
fi
testDir=solutions/ircode-solutions
file=$testDir/solution-irtest
for i in {0..4}
do
	echo "irtest$i" >> $file$i.txt
	echo "Solution >>>" >> $file$i.txt
	python3 -m goner.ircode Tests/irtest$i.g &>>  $file$i.txt	
	echo "<<<<" >> $file$i.txt
	echo "My implementation solution" >> $file$i.txt
	python3 -m gone.ircode Tests/irtest$i.g &>> $file$i.txt
done
