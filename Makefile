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

##################
# Useful targets #
##################

## Remove __pycache__.
remove_pycache:
	find . -type d -name __pycache__ -exec rm -r {} \+
.PHONY: remove pycache

##Run unittests.
run_unittests:
	python -m unittest discover -s .\tests\ -p '*_test.py'
.PHONY: remove pycache