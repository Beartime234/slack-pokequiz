#!/usr/bin/env bash

echo "Building Application"

DIST_FOLDER="dist"  # A folder that the distribution files live in. Just leave this
PYBUILD_FOLDER="py-build"

SRC="pokequiz"

# Get the requirements from pipenv
rm requirements.txt
pipenv lock -r > requirements.txt

# Make folders if they don't exist
mkdir -p ${DIST_FOLDER}
mkdir -p ${DIST_FOLDER}/${PYBUILD_FOLDER}

# Copy the actual code across
command cp -rf ${SRC} ${DIST_FOLDER}/${PYBUILD_FOLDER}/  # Go into this directory and make this flat

# install the requirements into a flat file structure
pipenv run pip install -r requirements.txt -t ${DIST_FOLDER}/${PYBUILD_FOLDER} --upgrade


