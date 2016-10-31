VERSION:=$(shell python setup.py --version)

clean:
	# Clean sources
	find dependency_injector -name '*.py[cod]' -delete
	find dependency_injector -name '__pycache__' -delete
	find dependency_injector -name '*.c' -delete
	find dependency_injector -name '*.so' -delete
	# Clean tests
	find tests -name '*.py[co]' -delete
	find tests -name '__pycache__' -delete
	# Clean examples
	find examples -name '*.py[co]' -delete
	find examples -name '__pycache__' -delete

compile: clean
	# Compile Cython to C
	cython -a dependency_injector/injections.pyx
	# Move all Cython html reports
	mkdir -p reports/cython/
	find dependency_injector -name '*.html' -exec mv {}  reports/cython/  \;

build: compile
	# Compile C extensions
	python setup.py build_ext --inplace

tests: build
	# Unit tests with coverage report
	coverage erase
	coverage run --rcfile=./.coveragerc -m unittest2 discover tests
	coverage report --rcfile=./.coveragerc
	coverage html --rcfile=./.coveragerc
	coverage erase
	# Static analysis
	flake8 --max-complexity=10 dependency_injector/
	flake8 --max-complexity=10 examples/
	# Code style analysis
	pydocstyle dependency_injector/
	pydocstyle examples/

publish: build tests
	# Create and upload build
	python setup.py sdist upload
	# Create and upload tag
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags
