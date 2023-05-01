# TIP_project
This project is part of technology innovation project

## project structure
```
├── README.md
├── APP
│   ├── manage.py
│   └── ...
├── DOCKER
│   ├── docker-compose.yml
│   └── ...
├── JUPYTER
│   ├── *.ipynb
│   └── PYTHON_MODULES
│       ├── __init__.py
│       └── ...
├── TEST
│   ├── test cases
│   └── ...

```

## Pre-requisites
1. docker
2. docker-compose
3. python3

## How to run the stack

### first time setup
```bash
docker-compose \
    -f ./DOCKER/docker-compose.yml  \
    --env-file .env \
    up --build
```
### spin up docker containers
```bash
docker-compose \
    -f ./DOCKER/docker-compose.yml  \
    --env-file .env \
    up
```
## Running django app
maybe
```bash
python ./APP/manage.py runserver
```

## running warehouse server

```bash
docker-compose -f ./DOCKER/docker-compose.warehouse.yml up --build
```

1. Go to http://localhost:8080/docs 
2. trigger aggregate data API with [1,2,3,5,10] to populate cache
3. go to http://localhost:8000/dataviz
   1. profit