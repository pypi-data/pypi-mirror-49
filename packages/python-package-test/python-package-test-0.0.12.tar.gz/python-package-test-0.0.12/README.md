# python-package-test

https://realpython.com/pypi-publish-python-package/

Test python package code


## Workflow

pip install wheel
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*