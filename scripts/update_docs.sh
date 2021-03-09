#!/bin/bash
if [[ $(git diff --stat) != '' ]]; then
        echo "Commit or discard all changes before updating docs"
        exit 1
fi
make -C docs clean
make -C docs html
cp -r docs/_build/html tmp
git checkout gh-pages
mv tmp/*.html .
rm -rf tmp/
git add .
git commit -m "Update docs"
git push
git checkout master
