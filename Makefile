.PHONY: clean source

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf build dist popcorns/popcorns.egg-info

source:
	python setup.py sdist bdist_wheel