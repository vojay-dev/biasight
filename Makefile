define BIASIGHT_LOGO
 _     _           _       _     _
| |   (_)         (_)     | |   | |
| |__  _  __ _ ___ _  __ _| |__ | |_
| '_ \| |/ _` / __| |/ _` | '_ \| __|
| |_) | | (_| \__ \ | (_| | | | | |_
|_.__/|_|\__,_|___/_|\__, |_| |_|\__|
                      __/ |
                     |___/
endef
export BIASIGHT_LOGO

.PHONY: all
all:
	@echo "$$BIASIGHT_LOGO"
	@echo "Run make help to see available commands"

.PHONY: help
help:
	@echo "$$BIASIGHT_LOGO"
	@echo "Available commands:"
	@echo "  make .venv          - Install dependencies using Poetry"
	@echo "  make run            - Run service locally"

.venv:
	@command -v poetry >/dev/null 2>&1 || { echo >&2 "Poetry is not installed"; exit 1; }
	poetry config virtualenvs.in-project true --local
	poetry install

.PHONY: run
run:
	poetry run fastapi dev biasight/main.py
