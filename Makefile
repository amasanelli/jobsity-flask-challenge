.PHONY: init build run db-migrate db-upgrade db-users test

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

db-migrate:
	docker-compose exec api-service /bin/sh -c 'cd /src; flask db migrate' 

db-upgrade:
	docker-compose exec api-service /bin/sh -c 'cd /src; flask db upgrade' 

db-users:
	docker-compose exec api-service /bin/sh -c 'cd /src; python commands.py' 

test:
	docker-compose run api-service /bin/sh -c 'cd /tests; python -m pytest' 
	docker-compose run stock-service /bin/sh -c 'cd /tests; python -m pytest'  

