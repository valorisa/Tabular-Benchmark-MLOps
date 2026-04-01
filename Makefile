.PHONY: install test lint clean train help

help:
@echo "Usage:"
@echo "  make install   - Install dependencies"
@echo "  make test      - Run pytest"
@echo "  make lint      - Run pre-commit"
@echo "  make clean     - Remove artifacts"
@echo "  make train     - Run benchmark"

install:
pip install -e .[dev]
pre-commit install

test:
pytest tests/ -v

lint:
pre-commit run --all-files

clean:
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .venv, __pycache__, build, dist, *.egg-info
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue logs, models

train:
python src/main.py --task classification --model all --epochs 50
