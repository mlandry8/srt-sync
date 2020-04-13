clean:
	@rm -rf build/ dist/ srtsync.egg-info/ venv/ __pycache__/

build:
	@python setup.py sdist bdist_wheel

upload_test:
	@python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

activate:
	@. venv/bin/activate

venv:
	@python -m venv ./venv;

runlocal: activate
	@venv/bin/python setup.py develop
