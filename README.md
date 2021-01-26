## A simple API that uses indexed text search on MongoDB

#### Dependencies OS:

docker
docker-compose

#### Install dependencies:

    make build

#### Run:

    make run

#### Insert text

    curl -X POST -H "Content-Type: application/json" \
    -d '{"key": "1", "title": "my title", "body": "my body"}' \
    http://localhost:8080/text

#### Get text by key

    key=1
    curl -X GET http://localhost:8080/text/$key

#### Search title and body

    curl -X GET http://localhost:8080/search?q=my%20title
        OR
    curl -X GET -G --data-urlencode "q=my title" http://localhost:8080/search

#### Run in dev mode:

    make run-dev

    Make sure MongoDB is running locally at 27017

#### Insert text

    curl -X POST -H "Content-Type: application/json" \
    -d '{"key": "1", "title": "my title", "body": "my body"}' \
    http://localhost:5000/text

#### Get text by key

    key=1
    curl -X GET http://localhost:5000/text/$key

#### Search title and body

    curl -X GET http://localhost:5000/search?q=my%20title
        OR
    curl -X GET -G --data-urlencode "q=my title" http://localhost:5000/search

#### For other commands

    make help
