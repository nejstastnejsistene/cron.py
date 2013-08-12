test %:
	@echo Testing Python 2
	@python -c "import sys,nose;sys.argv='nosetests -s tests/'.split();nose.main()"
	@echo Testing Python 3
	@python3 -c "import sys,nose;sys.argv='nosetests -s tests/'.split();nose.main()"

.PHONY: test
