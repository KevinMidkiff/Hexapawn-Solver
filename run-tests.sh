#!/bin/bash

function checkError {
    if [ $? -ne 0 ]
    then
        echo "Test $1 failed"
    else
        echo "Test $1 passed"
    fi
}


if [ $# -eq 1 ] ; then
    testDir="$1"
else
    testDir="tests"
fi

for test in `ls $testDir/*.in`
do
    name=$(echo `basename $test` | cut -f 1 -d '.')
    python3 hexapawn.py < $test 2> /dev/null > output.log
    diff output.log $testDir/$name.out
    checkError $name
done

