.PHONY: install generate-docs generate-questions run-pipeline test lint format dashboard api docker-up docker-down

install:
	python -m pip install -r requirements.txt

generate-docs:
	python -m src.data_generation.generate_documents

generate-questions:
	python -m src.data_generation.generate_golden_questions

run-pipeline:
	python -m src.pipeline.run_all

test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff format .

dashboard:
	python -m streamlit run src/dashboard/app.py

api:
	python -m uvicorn src.api.main:app --reload

docker-up:
	docker compose up --build

docker-down:
	docker compose down
