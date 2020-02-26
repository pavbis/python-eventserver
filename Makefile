.DEFAULT_GOAL := help
.SILENT:
.PHONY: vendor

## Colors
COLOR_RESET   = \033[0m
COLOR_INFO    = \033[32m
COLOR_COMMENT = \033[33m

## Help
help:
	printf "${COLOR_COMMENT}Usage:${COLOR_RESET}\n"
	printf " make [target]\n\n"
	printf "${COLOR_COMMENT}Available targets:${COLOR_RESET}\n"
	awk '/^[a-zA-Z\-\_0-9\.@]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf " ${COLOR_INFO}%-32s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

###############
## Var Block ##
###############
bin = docker-compose
runbackend = $(bin) run --rm backend

##################
# Useful targets #
##################

## Start docker containers.
dstart:
	$(bin) build --pull --parallel && $(bin) up -d --force-recreate
.PHONY: dstart

## Pull docker containers.
dpull:
	$(bin) pull
.PHONY: dpull

## Stop docker containers.
dstop:
	$(bin) down
.PHONY: dstop

## Remove unused docker data.
dclear:
	docker system prune --volumes --force
.PHONY: dclear

## Remove __pycache__.
remove_pycache:
	find . -type d -name __pycache__ -exec rm -r {} \+
.PHONY: remove_pycache

## Run pylint.
run_pylint:
	$(runbackend) pipenv run python -m pylint eventsserver/
.PHONY: run_pylint

## Run unit tests.
run_unittests:
	$(runbackend) pipenv run python -m unittest discover tests/unit/ -v
.PHONY: run_unittests

## Run integration tests.
run_interationtests:
	$(runbackend) pipenv run python -m unittest discover tests/integration/ -v
.PHONY: run_interationtests