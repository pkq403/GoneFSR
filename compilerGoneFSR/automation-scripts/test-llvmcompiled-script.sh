# Script written by Pedro Castro
#!/bin/bash
if ! [ -d ./solutions/llvmcompiled ]; then
	mkdir solutions/llvmcompiled
else 
	rm -r solutions/llvmcompiled
	mkdir solutions/llvmcompiled
fi
testDir=solutions/llvmcompiled
file=$testDir/solution-llvmcompile
for i in {0..4}
do
	echo "irtest$i" >> $file$i.txt
	echo "Solution >>>" >> $file$i.txt
	python3 -m goner.compile Tests/irtest$i.g 2> /dev/null
	./a.out >>  $file$i.txt	2> /dev/null
	echo "<<<<" >> $file$i.txt
	echo "My implementation solution" >> $file$i.txt
	python3 -m gone.compile Tests/irtest$i.g 2> /dev/null
	./a.out >> $file$i.txt 2> /dev/null
done
rm a.out
