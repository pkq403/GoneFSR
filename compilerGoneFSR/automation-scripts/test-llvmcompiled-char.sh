# Script written by Pedro Castro
#!/bin/bash
if ! [ -d ./solutions/llvmcompiled ]; then
	mkdir solutions/llvmcompiled
else 
	rm -r solutions/llvmcompiled
	mkdir solutions/llvmcompiled
fi
testDir=solutions/llvmcompiled
file=$testDir/solution-llvmcompile-char
echo "chartest" >> $file.txt
echo "Solution >>>" >> $file.txt
python3 -m goner.compile Tests/chartest.g 2> /dev/null
./a.out >>  $file.txt	2> /dev/null
echo "<<<<" >> $file.txt
echo "My implementation solution" >> $file.txt
python3 -m gone.compile Tests/chartest.g 2> /dev/null
./a.out >> $file$i.txt 2> /dev/null
rm a.out
