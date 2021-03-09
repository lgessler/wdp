#!/bin/bash
if [[ $(git diff --stat) != '' ]]; then
	echo "Commit or discard all changes before releasing"
	exit 1
fi
# check for version
if [ $# -eq 0 ]
then
	echo "Supply a version (e.g. 0.2.1)"
	exit 1
fi
# check for twine
if ! command -v twine &> /dev/null
then
	echo "twine could not be found (do you need to \`pip install twine\`?)"
	exit
fi

rm -rf build/ dist/
git tag -a "$1" -m "New release"
git push origin --tags
python setup.py bdist_wheel 
twine upload dist/*
