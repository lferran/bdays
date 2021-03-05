lint:
	venv/bin/isort bdays tests
	venv/bin/black bdays tests

lint-check:
	venv/bin/black -c bdays tests
	venv/bin/flake8 bdays tests --config=setup.cfg
