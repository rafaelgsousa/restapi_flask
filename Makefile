APP = restapi

test:
	@flake8 --exclude venv
	pytest -v --disable-warnings

up:
	@docker-compose down
	@docker-compose up

upde:
	@docker-compose down
	@docker-compose up -d

build:
	@docker-compose down
	@docker-compose up --build

buildde:
	@docker-compose down
	@docker-compose up --build -d