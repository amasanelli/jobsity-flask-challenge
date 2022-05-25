<div align="center">
    <img src="https://raw.githubusercontent.com/Jobsity/ReactChallenge/main/src/assets/jobsity_logo_small.png"/>
</div>

# Flask Challenge

## Description
This project is designed to test your knowledge of back-end web technologies, specifically in the Flask framework, Rest APIs, and decoupled services (microservices).

## Assignment
The goal of this exercise is to create a simple API using Flask to allow users to query [stock quotes](https://www.investopedia.com/terms/s/stockquote.asp).

The project consists of two separate services:
* A user-facing API that will receive requests from registered users asking for quote information.
* An internal stock aggregator service that queries external APIs to retrieve the requested quote information.

For simplicity, both services will share the same dependencies (requirements.txt) and can be run from the same virtualenv, but remember that they are still separate processes.

## Minimum requirements
### API service
* Endpoints in the API service should require authentication (no anonymous requests should be allowed). Each request should be authenticated via Basic Authentication.
You have to implement the code to check the user credentials are correct and put the right decorators around resource methods (check the auth.helpers module).
* When a user makes a request to get a stock quote (calls the stock endpoint in the api service), if a stock is found, it should be saved in the database associated to the user making the request.
* The response returned by the API service should be like this:

  `GET /stock?q=aapl.us`
  ```
    {
    "symbol": "AAPL.US",
    "company_name": "APPLE",
    "quote": 123
    }
  ```
  The quote value should be taken from the `close` field returned by the stock service.
* A user can get his history of queries made to the api service by hitting the history endpoint. The endpoint should return the list of entries saved in the database, showing the latest entries first:
  
  `GET /history`
  ```
  [
      {"date": "2021-04-01T19:20:30Z", "name": "APPLE", "symbol": "AAPL.US", "open": "123.66", "high": 123.66, "low": 122.49, "close": "123"},
      {"date": "2021-03-25T11:10:55Z", "name": "APPLE", "symbol": "AAPL.US", "open": "121.10", "high": 123.66, "low": 122, "close": "122"},
      ...
  ]
  ```
* A super user (and only super users) can hit the stats endpoint, which will return the top 5 most requested stocks:

  `GET /stats`
  ```
  [
      {"stock": "aapl.us", "times_requested": 5},
      {"stock": "msft.us", "times_requested": 2},
      ...
  ]
  ```
* All endpoint responses should be in JSON format.

### Stock service
* Assume this is an internal service, so requests to endpoints in this service don't need to be authenticated.
* When a stock request is received, this service should query an external API to get the stock information. For this challege, use this API: `https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv`.
* Note that `{stock_code}` above is a parameter that should be replaced with the requested stock code.
* You can see a list of available stock codes here: https://stooq.com/t/?i=518

## Architecture
![Architecture Diagram](diagram.svg)
1. A user makes a request asking for Apple's current Stock quote: `GET /stock?q=aapl.us`
2. The API service calls the stock service to retrieve the requested stock information
3. The stock service delegates the call to the external API, parses the response, and returns the information back to the API service.
4. The API service saves the response from the stock service in the database.
5. The data is formatted and returned to the user.

## Bonuses
The following features are optional to implement, but if you do, you'll be ranked higher in our evaluation process.
* Add unit tests for the bot and the main app.
* Connect the two services via RabbitMQ instead of doing http calls.
* Use JWT instead of basic authentication for endpoints.

## ~~How to run the project~~
* ~~Create a virtualenv: `python -m venv virtualenv` and activate it `. virtualenv/bin/activate`.~~
* ~~Install dependencies: `pip install -r requirements.txt`~~
* ~~Start the api service: `cd api_service ; flask db init ; flask db migrate; flask db upgrade ; flask run`~~
* ~~Start the stock service: `cd stock_service ; flask run`~~

__Important:__ If your implementation requires different steps to start the services
(like starting a rabbitMQ consumer), document them here!

---

## How to run the project
* Because the idea is to test my knowledge with microservices, I've decided to dockerize the services
* To run them use:
  ```
  docker-compose build

  docker-compose up -d

  docker-compose exec api-service /bin/sh -c 'cd src; DATABASE_URI=sqlite:///api_service.sqlite3 flask db stamp head'

  docker-compose exec api-service /bin/sh -c 'cd src; DATABASE_URI=sqlite:///api_service.sqlite3 flask db migrate' 

  docker-compose exec api-service /bin/sh -c 'cd src; DATABASE_URI=sqlite:///api_service.sqlite3 flask db upgrade' 

  docker-compose exec api-service /bin/sh -c 'cd src; DATABASE_URI=sqlite:///api_service.sqlite3 python commands.py init' 
  ```
* The previous commands have started up the db and created two users with the following data:
  ```python
  username="admin"
  email="admin@mail.com"
  password="admin"
  active=True
  role='ADMIN'
  ```
  ```python
  username="johndoe"
  email="johndoe@mail.com"
  password="john"
  active=True
  role='USER'
  ```

> PD: Replace `docker-compose build` with `docker-compose -f docker-compose-http.yml up` to run a project in which the services communicate by http requests

## How to use the project

* To login send a `POST` request to `http://127.0.0.1:5000/api/v1/login` whith the user data as a `JSON body`. For example:
  ```json
  {
      "username": "admin",
      "password": "admin"
  }
  ```
* Use the `token` retrieved in the previous step as a `Bearer token` authenticate and authorize your requests. You have to put it in the `Authorization header`
* Now you can send `GET` requests to the following endpoints:
  ```bash
  http://127.0.0.1:5000/api/v1/stock?q=aapl.us # change the stock code

  http://127.0.0.1:5000/api/v1/users/history

  http://127.0.0.1:5000/api/v1/stats
  ```

## How to test the project

* To test the api service
  - Start up the stock service and rabbitmq container run:
  ```
  docker run --rm -d -p 5672:5672 --name rabbit rabbitmq:management-alpine
  cd stock_service; python rpc_server.py
  ```
  - Open a new terminal and run:
  ```
  cd api_service/tests; pytest
  ```
* To test the stock service run:
  ```
  cd stock_service/tests; pytest
  ```
