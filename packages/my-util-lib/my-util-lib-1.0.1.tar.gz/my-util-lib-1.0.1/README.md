<h3>Memo</h3>
**Run unit tests before packaging library**

python setup.py pytest

**Packaging library**

!! Make sure my_util_library.egg-info folder is removed.
python setup.py sdist

**Check the content in the library package**

tar --list -f dist/my-util-lib-1.0.0.tar.gz

**Publish package on Pypi**

!! Package name should be unique, and the name can never be reused even though package is delete from Pypi.
twine upload dist/*
