#!/bin/bash
if ! [ -d ./solutions/llvmgen-solutions ]; then
	mkdir solutions/llvmgen-solutions
else 
	rm -r solutions/llvmgen-solutions
	mkdir solutions/llvmgen-solutions
fi
testDir=solutions/llvmgen-solutions
file=$testDir/solution-llvmgen
for i in {0..4}
do
	echo "llvmgen-test$i" >> $file$i.txt
	echo "Solution >>>" >> $file$i.txt
	python3 -m goner.llvmgen Tests/irtest$i.g >>  $file$i.txt 2> /dev/null	
	echo "<<<<" >> $file$i.txt
	echo "My implementation solution" >> $file$i.txt
	python3 -m gone.llvmgen Tests/irtest$i.g >> $file$i.txt  2> /dev/null
done
