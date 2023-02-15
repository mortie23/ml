#!/usr/bin/bash

project=${1}
echo ${project}

# sync the shared lib to the project
rsync -avu --delete "../../lib/" "../../${project}/${project}/lib"
# create a temp pyproject.toml that references the project local lib
cp ../../${project}/${project}/pyproject.toml ../../${project}/${project}/pyproject-tmp.toml
sed -i 's/..\/..\///' ../../${project}/${project}/pyproject.toml
sed -i 's/, develop = true//' ../../${project}/${project}/pyproject.toml

docker build -t mortimerxyz/flaskapp1:0.0.1 ../../${project}/${project}/

rm ../../${project}/${project}/pyproject.toml
mv ../../${project}/${project}/pyproject-tmp.toml ../../${project}/${project}/pyproject.toml
