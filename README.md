## A simple API that uses indexed text search on MongoDB

#### Dependencies OS:

docker
docker-compose

#### Install dependencies:

    make build

#### Run:

    make run

#### Insert document

    curl -X POST -H "Content-Type: application/json" \
    -d '{"key": "1", "title": "my title", "body": "my body"}' \
    http://localhost:8080/document

#### Get document by key

    Key is a URL param

    key=1
    curl -X GET http://localhost:8080/document/$key

#### Search documents

    String to be searched is a URL param

    Search will occur on title and body

    search_string=my%20title
    curl -X GET http://localhost:8080/documents/$search_string

#### Run in dev mode:

    make run-dev

    Make sure MongoDB is running locally at 27017

#### Insert document

    curl -X POST -H "Content-Type: application/json" \
    -d '{"key": "1", "title": "my title", "body": "my body"}' \
    http://localhost:5000/document

#### Get document by key

    Key is a URL param

    key=1
    curl -X GET http://localhost:5000/document/$key

#### Search documents

    String to be searched is a URL param

    Search will occur on title and body

    search_string=my%20title
    curl -X GET http://localhost:5000/documents/$search_string

#### For other commands

    make help
