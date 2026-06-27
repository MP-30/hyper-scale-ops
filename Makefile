help:
	@echo "Available commands:"
	@echo "  make install                     Install dependencies"
	@echo "  make run                         Run FastAPI server"
	@echo "  make migration msg='message'     Create migration"
	@echo "  make upgrade                     Apply migrations"
	@echo "  make downgrade                   Rollback one migration"
	@echo "  make current                     Show current migration"
	@echo "  make history                     Show migration history"
	@echo "  make clean                       Remove cache files"
hello:
	@echo "Hello Aditya! Your Makefile is working perfectly."

install:
	uv sync

run:
	uv run uvicorn app.main:app --reload

migration:
	uv run alembic revision --autogenerate -m "$(msg)"

upgrade:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade -1

current:
	uv run alembic current

history:
	uv run alembic history

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker_start:
	docker build -t my-project-img:v1 .
	docker run -d --name my-project-cont --env-file .env -p 8000:8000 my-project-img:v1

docker_clean:
	docker stop my-project-cont
	docker rm my-project-cont
	docker rmi my-project-img