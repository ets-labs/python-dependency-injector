VERSION := $(shell python setup.py --version)

CYTHON_SRC := $(shell find dependency_injector -name '*.pyx')

CYTHON_DIRECTIVES =

ifdef DEPENDENCY_INJECTOR_DEBUG_MODE
	CYTHON_DIRECTIVES += -Xprofile=True
	CYTHON_DIRECTIVES += -Xlinetrace=True
endif


clean:
	# Clean sources
	find dependency_injector -name '*.py[cod]' -delete
	find dependency_injector -name '__pycache__' -delete
	find dependency_injector -name '*.c' -delete
	find dependency_injector -name '*.so' -delete
	find dependency_injector -name '*.html' -delete
	# Clean tests
	find tests -name '*.py[co]' -delete
	find tests -name '__pycache__' -delete
	# Clean examples
	find examples -name '*.py[co]' -delete
	find examples -name '__pycache__' -delete

cythonize:
	# Compile Cython to C
	cython -a $(CYTHON_DIRECTIVES) $(CYTHON_SRC)
	# Move all Cython html reports
	mkdir -p reports/cython/
	find dependency_injector -name '*.html' -exec mv {}  reports/cython/  \;

build: clean cythonize
	# Compile C extensions
	python setup.py build_ext --inplace

test:
	# Unit tests with coverage report
	coverage erase
	coverage run --rcfile=./.coveragerc -m unittest2 discover tests
	coverage report --rcfile=./.coveragerc
	coverage html --rcfile=./.coveragerc

check:
	# Static analysis
	flake8 --max-complexity=10 dependency_injector/
	flake8 --max-complexity=10 examples/
	# Code style analysis
	pydocstyle dependency_injector/
	pydocstyle examples/

publish: cythonize
	# Create and upload build
	python setup.py sdist upload
	# Create and upload tag
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags
