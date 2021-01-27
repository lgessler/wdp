Release
=======

Upload to PyPI
--------------

.. code-block:: bash

    # clean previous builds
    rm -rf build/ dist/
    # tag the release
    git tag -a x.y.z -m "release notes"
    # don't forget to push the tag
    git push origin --tags
    # check the tag
    python setup.py --version
    # build
    python setup.py bdist_wheel
    # test on testpypi
    twine upload --repository testpypi dist/*
    # upload to pypi
    twine upload dist/*

Update Docs
-----------

.. code-block:: bash

    make -C docs html
    cp -r docs/_build/html tmp
    git checkout gh-pages
    mv tmp/*.html .
    rm -rf tmp/
    git add .
    git commit -m "Update docs"
    git push
    git checkout master