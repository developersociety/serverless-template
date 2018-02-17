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

clean: ## Remove unneeded files generated from the various build tasks.
clean: coverage-clean

reset: ## Reset your local environment. Useful after switching branches, etc.
reset: venv-check venv-wipe install-local

clear: ## Like reset but without the wiping of the installs.
clear: ;

check: ## Check for any obvious errors in the project's setup.
check: pipdeptree-check

format: ## Run this project's code formatters.
format: yapf-format isort-format

lint: ## Lint the project.
lint: yapf-lint isort-lint flake8-lint

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
	if ! pip list --format=freeze | grep -v "^appdirs=\|^distribute=\|^packaging=\|^pip=\|^pyparsing=\|^setuptools=\|^six=\|^wheel=" | xargs pip uninstall -y; then \
	    echo "Nothing to remove"; \
	fi


# Installs
install-local: pip-install-local


# Pip
pip-install-local: venv-check
	pip install -r requirements/local.txt


# Fabfile
fab-deploy:
	fab deploy


# ISort
isort-version:
	isort --version

isort-lint: isort-version
	isort --recursive --check-only --diff {{ cookiecutter.project_slug }} tests

isort-format: isort-version
	isort --recursive {{ cookiecutter.project_slug }} tests


# Flake8
flake8-lint:
	flake8 {{ cookiecutter.project_slug }} tests


# Coverage
coverage-report: coverage-html coverage-xml
	coverage report --show-missing

coverage-html:
	coverage html

coverage-xml:
	coverage xml

coverage-clean:
	rm -rf htmlcov
	rm -rf reports
	rm -f .coverage


# Project testing
pytest-test:
	coverage run -m pytest


# YAPF
yapf-lint:
	yapf_lint_output="`yapf -r -p -d --style .style.yapf {{ cookiecutter.project_slug }} tests`" && \
	if [[ $$yapf_lint_output ]]; then echo -e "$$yapf_lint_output"; exit 1; fi

yapf-format:
	yapf -r -i -p --style .style.yapf {{ cookiecutter.project_slug }} tests


#pipdeptree
pipdeptree-check:
	pipdeptree --warn fail > /dev/null


# Local server
flask-serve:
	FLASK_APP={{ cookiecutter.project_slug }} FLASK_DEBUG=1 python -m flask run


# Help
help-display:
	@awk '/^[[:alnum:]-]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)
