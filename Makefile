.PHONY: help install run test lint format migrate seed clean docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make run         - Run development server"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make migrate     - Run database migrations"
	@echo "  make seed        - Seed database with initial data"
	@echo "  make clean       - Clean cache files"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	flake8 app tests
	mypy app

format:
	black app tests
	isort app tests

migrate:
	alembic upgrade head

seed:
	python seeds/seed_users.py

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
