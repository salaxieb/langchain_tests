include .env

start:
	@python assistant/main.py

lint:
	@poetry run mypy assistant
	@poetry run pylint assistant
	@poetry run flake8 assistant
	@poetry run black assistant --check


test:
	@poetry run pytest


tox:
	@poetry run tox


requirements:
	@poetry export -f requirements.txt --output requirements.txt
	@poetry export -f requirements.txt --output requirements.dev.txt --dev


clean:
	@rm -rf .mypy_cache
	@rm -rf .tox
	@rm -rf .pytest_cache
