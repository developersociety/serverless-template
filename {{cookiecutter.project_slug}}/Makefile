SHELL=/bin/bash
.DEFAULT_GOAL := help


# ---------------------------------
# Project specific targets
# ---------------------------------
#
# Add any targets specific to the current project in here.



# -------------------------------
# Common targets for Dev projects
# -------------------------------
#
# Edit these targets so they work as expected on the current project.
#
# Remember there may be other tools which use these targets, so if a target is not suitable for
# the current project, then keep the target and simply make it do nothing.

help: ## This help dialog.
help: help-display

nuke: ## Full wipe of the local environment, uncommitted files, and database.
nuke: venv-check venv-wipe git-full-clean

reset: ## Reset your local environment. Useful after switching branches, etc.
reset: venv-check venv-wipe install-local

clear: ## Like reset but without the wiping of the installs.
clear: ;

check: ## Check for any obvious errors in the project's setup.
check: uv-check npm-check

format: ## Run this project's code formatters.
format: ruff-format

lint: ## Lint the project.
lint: ruff-lint

test: ## Run unit and integration tests.
test: pytest-test

test-report: ## Run and report on unit and integration tests.
test-report: coverage-clean test coverage-report

serve: ## Run a local development server.
serve: flask-serve

deploy: ## Deploy this project to demo or live.
deploy: fab-deploy



# ---------------
# Utility targets
# ---------------
#
# Targets which are used by the common targets. You likely want to customise these per project,
# to ensure they're pointing at the correct directories, etc.

# Virtual Environments
venv-check:
ifndef VIRTUAL_ENV
	$(error Must be in a virtualenv)
endif

venv-wipe: venv-check
	uv pip freeze | uv pip uninstall -r -


# Destructive cleaning
git-full-clean:
	git clean -ffdx


# Installs
install-local: npm-install uv-install-local


# UV
uv-install-local: venv-check
	uv sync --active --frozen --dev

uv-upgrade: venv-check
	uv lock --upgrade

uv-check: venv-check
	uv lock --check


# Fabfile
fab-deploy:
	fab $${site:-live} deploy


# Coverage
coverage-report: coverage-html
	coverage report --show-missing

coverage-html:
	coverage html

coverage-clean:
	rm -rf htmlcov
	rm -f .coverage


# Project testing
pytest-test:
	PYTHONWARNINGS=all coverage run -m pytest


# NPM
npm-check: npm-install

npm-install:
	cmp --silent package-lock.json node_modules/.package-lock.json || (npm ci && cp -a package-lock.json node_modules/.package-lock.json)


# Ruff
ruff-lint:
	ruff check
	ruff format --check

ruff-format:
	ruff check --fix-only
	ruff format


# Local server
flask-serve:
	FLASK_APP=project FLASK_DEBUG=1 python -m flask run


# Help
help-display:
	@awk '/^[\-[:alnum:]]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)
