
install:
	pip install flake8
	pip install mypy
	pip install pygame

run:
	python fly_in.py maps/network_of_drones.txt

debug:
	python -m pdb fly_in.py maps/network_of_drones.txt

clean:
	rm -rf */__pycache__ .mypy_cache */.mypy_cache */.pytest_cache */build dist */*.egg-info poetry.lock

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
