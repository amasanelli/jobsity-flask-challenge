.PHONY: init build run db-migrate db-upgrade db-users

init:  
	build 
	run
	db-migrate
	db-upgrade
	db-users
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-stamp-head:
	docker-compose exec api-service /bin/sh -c 'cd src; DATABASE_URI=sqlite:///api_service.sqlite3 flask db stamp head'

db-migrate:
	docker-compose exec api-service /bin/sh -c 'cd src; DATABASE_URI=sqlite:///api_service.sqlite3 flask db migrate' 

db-upgrade:
	docker-compose exec api-service /bin/sh -c 'cd src; DATABASE_URI=sqlite:///api_service.sqlite3 flask db upgrade' 

db-users:
	docker-compose exec api-service /bin/sh -c 'cd src; DATABASE_URI=sqlite:///api_service.sqlite3 python commands.py init' 

