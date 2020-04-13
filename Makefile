

clean:
	@rm -rf build/ dist/ srtsync.egg-info/

build:
	@python setup.py sdist bdist_wheel

upload:
	@python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*