init:
	pipenv install

test:
	pipenv run nosetests kindle_tools

shell:
	pipenv shell