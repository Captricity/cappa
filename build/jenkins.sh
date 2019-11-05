#!/bin/bash
GITHUB_TOKEN=$1
DEBUG=$2
if [ -z ${WORKSPACE} ] || [ -z ${JOB_NAME} ]; then
    ExampleENV="`pwd`/venv"
else
    ExampleENV="${WORKSPACE}/.${JOB_NAME}Env"
fi

if [ -d ${ExampleENV} ]; then
    rm -rf ${ExampleENV}
fi

echo "##############################################################"
echo "# Creating VirtualEnv ########################################"
echo "##############################################################"
virtualenv --python=python2.7 "${ExampleENV}"
source ${ExampleENV}/bin/activate

echo -e "\n##############################################################"
echo "# Installing Cappa #######################################"
echo "##############################################################"
python setup.py install

echo -e "\n##############################################################"
echo "# Checking Python Packages Security ######################"
echo "##############################################################"
pip install -q safety
safety check --full-report

echo -e "\n##############################################################"
echo "# Performing Style Checks ####################################"
echo "##############################################################"
pip install -q flake8
flake8 cappa/

echo -e "\n##############################################################"
echo "# Running unit tests #########################################"
echo "##############################################################"
(cd `pwd`/tests/serverspecs/ && sh ./test_all.sh ${GITHUB_TOKEN} ${DEBUG})

deactivate
if [ -d ${ExampleENV} ]; then
    rm -rf ${ExampleENV}
fi