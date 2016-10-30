VERSION:=$(shell python setup.py --version)

publish:
	python setup.py sdist upload
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags
