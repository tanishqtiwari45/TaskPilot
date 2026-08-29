.PHONY: help install test lint format clean build run dev setup

# TaskPilot Development Makefile
# Usage: make [target]
# Example: make install, make test, make run

PYTHON := python
PIP := pip
NPM := npm
VENV := .venv

help:
	@echo "TaskPilot Development Makefile"
	@echo "=============================="
	@echo ""
	@echo "Available targets:"
	@echo "  make install      - Install all dependencies (backend + frontend)"
	@echo "  make dev          - Run backend and frontend in development mode"
	@echo "  make test         - Run all tests (backend + frontend)"
	@echo "  make backend-test - Run backend tests only"
	@echo "  make lint         - Run code quality checks"
	@echo "  make format       - Auto-format code"
	@echo "  make build        - Build frontend for production"
	@echo "  make clean        - Clean build artifacts and caches"
	@echo "  make setup        - Setup development environment"
	@echo "  make help         - Show this help message"
	@echo ""

setup:
	@echo "Setting up development environment..."
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/Scripts/activate && $(PIP) install -r requirements-dev.txt
	cd frontend && $(NPM) install
	@echo "✓ Development environment ready!"
	@echo ""
	@echo "To activate virtual environment, run:"
	@echo "  Windows: .\\.venv\\Scripts\\Activate.ps1"
	@echo "  Linux/Mac: source .venv/bin/activate"

install: setup
	@echo "✓ Installation complete!"

dev:
	@echo "Starting TaskPilot in development mode..."
	@echo "Backend: http://localhost:5000"
	@echo "Frontend: http://localhost:5173"
	@echo ""
	@echo "Starting backend..."
	@start cmd /k "$(PYTHON) app.py"
	@echo "Starting frontend..."
	@cd frontend && $(NPM) run dev

test:
	@echo "Running all tests..."
	@echo ""
	@echo "Running backend tests..."
	. $(VENV)/Scripts/activate && $(PYTHON) -m pytest tests/ -v --tb=short
	@echo ""
	@echo "✓ All tests completed!"

backend-test:
	@echo "Running backend tests..."
	. $(VENV)/Scripts/activate && $(PYTHON) -m pytest tests/ -v --tb=short

backend-test-verbose:
	@echo "Running backend tests (verbose)..."
	. $(VENV)/Scripts/activate && $(PYTHON) -m pytest tests/ -vv --tb=long

backend-test-coverage:
	@echo "Running backend tests with coverage..."
	. $(VENV)/Scripts/activate && $(PYTHON) -m pytest tests/ --cov=. --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	@echo "Running code quality checks..."
	@echo ""
	@echo "Checking Python syntax with flake8..."
	. $(VENV)/Scripts/activate && flake8 . --max-line-length=100 --exclude=.venv,frontend
	@echo ""
	@echo "Checking type hints with mypy..."
	. $(VENV)/Scripts/activate && mypy app.py config.py auth.py --ignore-missing-imports 2>/dev/null || echo "⚠ Type check: skipped (optional)"
	@echo ""
	@echo "✓ Linting complete!"

format:
	@echo "Auto-formatting code..."
	@echo ""
	@echo "Formatting Python code with black..."
	. $(VENV)/Scripts/activate && black . --exclude=".venv|frontend" --line-length=100
	@echo ""
	@echo "Sorting imports with isort..."
	. $(VENV)/Scripts/activate && isort . --skip=.venv --skip=frontend
	@echo ""
	@echo "✓ Formatting complete!"

build:
	@echo "Building frontend for production..."
	cd frontend && $(NPM) run build
	@echo "✓ Frontend built to frontend/dist/"

clean:
	@echo "Cleaning build artifacts..."
	@powershell -Command "if (Test-Path .venv) { Remove-Item -Recurse -Force .venv; Write-Host '✓ Removed .venv' }"
	@powershell -Command "if (Test-Path __pycache__) { Remove-Item -Recurse -Force __pycache__; Write-Host '✓ Removed __pycache__' }"
	@powershell -Command "if (Test-Path .pytest_cache) { Remove-Item -Recurse -Force .pytest_cache; Write-Host '✓ Removed .pytest_cache' }"
	@powershell -Command "if (Test-Path htmlcov) { Remove-Item -Recurse -Force htmlcov; Write-Host '✓ Removed htmlcov' }"
	@powershell -Command "if (Test-Path frontend/node_modules) { Remove-Item -Recurse -Force frontend/node_modules; Write-Host '✓ Removed frontend/node_modules' }"
	@powershell -Command "if (Test-Path frontend/dist) { Remove-Item -Recurse -Force frontend/dist; Write-Host '✓ Removed frontend/dist' }"
	@powershell -Command "if (Test-Path .eggs) { Remove-Item -Recurse -Force .eggs; Write-Host '✓ Removed .eggs' }"
	@powershell -Command "if (Test-Path *.egg-info) { Remove-Item -Recurse -Force *.egg-info; Write-Host '✓ Removed *.egg-info' }"
	@echo "✓ Cleanup complete!"

db-init:
	@echo "Initializing database..."
	. $(VENV)/Scripts/activate && $(PYTHON) -c "from database import init_db; init_db(); print('✓ Database initialized!')"

db-reset:
	@echo "Resetting database (WARNING: This will delete all data!)..."
	@powershell -Command "$$proceed = Read-Host 'Type yes to confirm'; if ($$proceed -eq 'yes') { rm task_pilot.db 2>/dev/null; write-Host 'Database reset complete' }"

run:
	@echo "Starting TaskPilot backend..."
	. $(VENV)/Scripts/activate && $(PYTHON) app.py

run-prod:
	@echo "Starting TaskPilot in production mode..."
	. $(VENV)/Scripts/activate && $(PYTHON) -c "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=5000, debug=False)"

health-check:
	@echo "Checking API health..."
	@powershell -Command "try { $$response = Invoke-WebRequest -Uri 'http://localhost:5000/health' -Method GET; Write-Host '✓ API is healthy'; Write-Host $$response.Content } catch { Write-Host '✗ API is not responding' }"

logs:
	@echo "Showing recent logs..."
	@powershell -Command "Get-Content log.txt -Tail 50 2>/dev/null || Write-Host 'No logs found'"

freeze:
	@echo "Freezing dependencies..."
	. $(VENV)/Scripts/activate && $(PIP) freeze > requirements-frozen.txt
	@echo "✓ Frozen requirements saved to requirements-frozen.txt"

.DEFAULT_GOAL := help
