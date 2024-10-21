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
	@echo "  make test           - Run tests"
	@echo "  make ruff           - Run linter"
	@echo "  make check          - Run tests and linter"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-start   - Start BiaSight API with Docker"
	@echo "  make docker-stop    - Stop BiaSight API Docker container"
	@echo "  make docker-logs    - Tail logs of BiaSight API Docker container"
	@echo "  make clean          - Remove latest build artifact"
	@echo "  make build          - Build artifact for deployment"

.venv:
	@command -v poetry >/dev/null 2>&1 || { echo >&2 "Poetry is not installed"; exit 1; }
	poetry config virtualenvs.in-project true --local
	poetry install

.PHONY: run
run:
	poetry run fastapi dev biasight/main.py

.PHONY: test
test:
	poetry run python -m pytest tests/ -v -Wignore

.PHONY: ruff
ruff:
	poetry run ruff check --fix

.PHONY: check
check: test ruff

.PHONY: docker-build
docker-build:
	docker build -t biasight .

.PHONY: docker-start
docker-start: docker-build
	docker run -d --rm --name biasight -p 9091:9091 biasight
	@echo "BiaSight API running on port 9091"

.PHONY: docker-stop
docker-stop:
	@if [ $$(docker ps -q -f name=biasight) ]; then \
		echo "Stopping biasight container..."; \
		docker stop biasight; \
	else \
		echo "Container biasight is not running"; \
	fi

.PHONY: docker-logs
docker-logs:
	@if [ $$(docker ps -q -f name=biasight) ]; then \
		docker logs -f biasight; \
	else \
		echo "Container biasight is not running"; \
	fi

.PHONY: clean
clean:
	rm -rf biasight_latest.tar.gz

.PHONY: build
build: clean
	docker image rm biasight
	docker build -t biasight .
	docker save biasight:latest | gzip > biasight_latest.tar.gz
