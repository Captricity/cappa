#!/bin/bash

# Usage: test.sh tsd json <GITHUB_TOKEN> keep
MODULE=$1
EXT=$2
GITHUB_TOKEN=$3
KEEP=$4

if [[ (${MODULE} == "captricity" && -z ${GITHUB_TOKEN}) ]]; then 
    echo "Missing GITHUB_TOKEN for Captricity test."
    exit 1
fi

container_name=test_${MODULE}_${EXT}

docker stop ${container_name}
docker container rm ${container_name}
docker run -dit --name ${container_name} cappa

echo "Installing cappa : ${container_name}"
docker exec -i ${container_name} bash -c "export GITHUB_TOKEN=${GITHUB_TOKEN} && cappa install --private-https-oauth --save-js --no-venv -r tests/serverspecs/test_install_${MODULE}.${EXT}"

echo "Test results : ${container_name}"
docker exec -i ${container_name} bash -c "cd /cappa-master/tests/serverspecs/ && rake spec SPEC=spec/default/${MODULE}_install_spec.rb"

exit_status=$?
if [[ ${exit_status} -eq 0 ]]; then
    echo "${container_name} PASSED!"
else
    echo "${container_name} FAILED!"
fi

if [[ ${KEEP} != "debug" ]]; then
    docker stop ${container_name}
    docker container rm ${container_name}
fi
exit ${exit_status}