VERSION := $(shell python setup.py --version)

CYTHON_SRC := $(shell find src/dependency_injector -name '*.pyx')

CYTHON_DIRECTIVES =

ifdef DEPENDENCY_INJECTOR_DEBUG_MODE
	CYTHON_DIRECTIVES += -Xprofile=True
	CYTHON_DIRECTIVES += -Xlinetrace=True
endif


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

cythonize:
	# Compile Cython to C
	cython -a $(CYTHON_DIRECTIVES) $(CYTHON_SRC)
	# Move all Cython html reports
	mkdir -p reports/cython/
	find src -name '*.html' -exec mv {}  reports/cython/  \;

build: clean cythonize
	# Compile C extensions
	python setup.py build_ext --inplace

install: uninstall clean cythonize
	pip install -ve .

uninstall:
	- pip uninstall -y -q dependency-injector 2> /dev/null

test: build
	# Unit tests with coverage report
	coverage erase
	coverage run --rcfile=./.coveragerc -m unittest2 discover tests/unit
	coverage report --rcfile=./.coveragerc
	coverage html --rcfile=./.coveragerc

check:
	# Static analysis
	flake8 --max-complexity=10 src/dependency_injector/
	flake8 --max-complexity=10 examples/
	# Code style analysis
	pydocstyle src/dependency_injector/
	pydocstyle examples/

publish: cythonize
	# Merge release to master branch
	git checkout master
	git merge --no-ff release/$(VERSION) -m 'Merge branch release/$(VERSION)'
	git push origin master
	# Create and upload tag
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags
	# Create and upload build
	python setup.py sdist upload
