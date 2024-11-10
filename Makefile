VERSION := $(shell python setup.py --version)

export COVERAGE_RCFILE := pyproject.toml

clean:
	# Clean sources
	find src -name '*.py[cod]' -delete
	find src -name '__pycache__' -delete
	find src -name '*.c' -delete
	find src -name '*.h' -delete
	find src -name '*.so' -delete
	find src -name '*.html' -delete
	# Clean tests
	find tests -name '*.py[co]' -delete
	find tests -name '__pycache__' -delete
	# Clean examples
	find examples -name '*.py[co]' -delete
	find examples -name '__pycache__' -delete

build: clean
	# Compile C extensions
	python setup.py build_ext --inplace
	# Move all Cython html reports
	mkdir -p reports/cython/
	find src -name '*.html' -exec mv {}  reports/cython/  \;

docs-live:
	sphinx-autobuild docs docs/_build/html

install: uninstall clean build
	pip install -ve .

uninstall:
	- pip uninstall -y -q dependency-injector 2> /dev/null

test:
	# Unit tests with coverage report
	coverage erase
	coverage run -m pytest -c tests/.configs/pytest.ini
	coverage report
	coverage html

check:
	flake8 src/dependency_injector/
	flake8 examples/

	pydocstyle src/dependency_injector/
	pydocstyle examples/

	mypy tests/typing

test-publish: build
	# Create distributions
	python -m build --sdist
	# Upload distributions to PyPI
	twine upload --repository testpypi dist/dependency-injector-$(VERSION)*

publish:
	# Merge release to master branch
	git checkout master
	git merge --no-ff release/$(VERSION) -m "Merge branch 'release/$(VERSION)' into master"
	git push origin master
	# Create and upload tag
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags
