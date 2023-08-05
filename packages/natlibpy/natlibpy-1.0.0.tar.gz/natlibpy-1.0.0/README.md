# natlibpy

## Links

- [PyPI](https://pypi.org/project/natlibpy/)
- [GitHub](https://github.com/narthur/natlibpy)

## Development

- Set up a virtual environment in PyCharm so you aren't using the global Python env. This will allow you to avoid
conflicts of dependencies.
- `pip install twine wheel`

## Deployment

- Update version number in `setup.py`
- `python setup.py sdist bdist_wheel`
- Check that expected files are included: `tar tzf dist/pyminder-{ version }.tar.gz`
- `twine check dist/*`
- Test publish: `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
- Publish: `twine upload dist/*`

## Information

- [How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)
- [Building and Distributing Packages with Setuptools](https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use)