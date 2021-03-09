#!/bin/bash
if [[ $(git diff --stat) != '' ]]; then
        echo "Commit or discard all changes before updating docs"
        exit 1
fi
# build the docs and move to a tmp folder
make -C docs clean
make -C docs html
cp -r docs/_build/html tmp

# checkout github pages branch
git checkout gh-pages

# clear existing pages and copy new content
rm -rf _modules/ _sources/ _static/ api
mv tmp/{*.html,_modules/,_sources/,_static/,api} .
# remove temp folder
rm -rf tmp/
# commit and push
git add .
git commit -m "Update docs"
git push

# return to master and clean up
git checkout master
make -C docs clean
