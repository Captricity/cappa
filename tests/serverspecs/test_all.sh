#!/bin/bash

fails=()
GITHUB_TOKEN=$1
DEBUG=$2

if [[ ${GITHUB_TOKEN} == "" ]]; then
    echo "Error: Missing GITHUB_TOKEN."
    echo "Usage: ./test_all.sh <GITHUB_TOKEN> debug"
    exit 1
fi  
for i in $(find . -type f -name "*.json" -o -name "*.yaml")
do
    [[ $i =~ ^(./test_install_)(.*) ]]    
    test=${BASH_REMATCH[2]}
    filename=$(echo $test | cut -f1 -d.)
    ext=$(echo $test | cut -f2 -d.)
    sh ./test.sh ${filename} ${ext} ${GITHUB_TOKEN} ${debug}
    if [[ $? != 0 ]]; then 
        echo "FAIL!"
        fails+="${filename}_${ext}"
    fi
done
echo "****************************************************************************************************************"
if [ ${#fails[@]} == 0 ]; then 
    echo "All tests PASS!"
else
    echo "FAILURES: "
    printf "%s" "${fails[@]}"
fi
echo ""
echo "****************************************************************************************************************"