
install:
	pip install flake8
	pip install mypy
	pip install poetry
	pip install pygame
	poetry install

run:
	python3 main.py

debug:
	python -m pdb main.py

clean:
	rm -rf */__pycache__ .mypy_cache */.mypy_cache */.pytest_cache */build dist */*.egg-info poetry.lock

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
