#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "No argument supplied."
    echo "Usage:"
    echo "./build <app-name>"
    exit 1
fi

project=${1}
echo ${project}

# sync the shared lib to the project
rsync -avu --delete "../../lib/" "../../app/${project}/lib"
# create a temp pyproject.toml that references the project local lib
cp ../../app/${project}/pyproject.toml ../../app/${project}/pyproject-tmp.toml
sed -i 's/..\/..\///' ../../app/${project}/pyproject.toml
sed -i 's/, develop = true//' ../../app/${project}/pyproject.toml

docker build -t mortimerxyz/flaskapp1:0.0.1 ../../app/${project}/

rm ../../app/${project}/pyproject.toml
mv ../../app/${project}/pyproject-tmp.toml ../../app/${project}/pyproject.toml
