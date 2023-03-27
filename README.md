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
### spin up docker containers
```bash
docker-compose -f ./DOCKER/docker-compose.yml up -d
```
## Running django app
maybe
```bash
python ./APP/day16/manage.py runserver
```