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
├── WAREHOUSE
│   ├── fastapiAPP
│   └── ...

```

## Pre-requisites
1. docker
2. docker-compose
3. python3

## How to run the stack

### running the app server
1. configure .env file
```bash
cp ./DOCKER/.env.example ./DOCKER/.env
```

2. edit the file

3. build and run the stack
```bash
docker-compose -f ./DOCKER/docker-compose.yml up --build
```


#### if in doubt
run this command to remove the persistent docker container and volumes with new .env settings
```bash
docker-compose -f ./DOCKER/docker-compose.yml down -v
```
