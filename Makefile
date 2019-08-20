debug:
	python ./api/api.py --debug True

test:
	pytest ./tests/ --cov=api tests/

run:
	python ./api/api.py --debug False
