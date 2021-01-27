#!/bin/bash
make -C docs html
cp -r docs/_build/html tmp
git checkout gh-pages
mv tmp/*.html
rm -rf tmp/
git add .
git commit -m "update docs"
git push
git checkout master
