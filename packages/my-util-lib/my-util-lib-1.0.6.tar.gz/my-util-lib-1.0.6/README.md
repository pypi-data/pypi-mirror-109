<h3>Memo</h3>
**Run unit tests before packaging library**

python setup.py pytest

**Packaging library**

!! Make sure my_util_library.egg-info folder is removed.
python setup.py sdist

**Check the content in the library package**

tar --list -f dist/my-util-lib-1.0.0.tar.gz

**Publish package on Pypi**

!! Package name should be unique, and the name can never be reused even though package is delete from Pypi.<br />
twine upload dist/*

pip3 install . -vvv<br />

python3 setup.py bdist_wheel<br />
python3 setup.py sdist bdist_wheel<br />
pip3 install -e .


https://stackoverflow.com/questions/50585246/pip-install-creates-only-the-dist-info-not-the-package <br />
https://www.youtube.com/watch?v=GIF3LaRqgXo