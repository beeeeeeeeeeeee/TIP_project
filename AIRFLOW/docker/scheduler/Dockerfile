FROM apache/airflow:latest-python3.10

USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    libgeos-dev \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt




