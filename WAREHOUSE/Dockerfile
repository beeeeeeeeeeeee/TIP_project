FROM continuumio/miniconda3

WORKDIR /code

# 

RUN pip install --upgrade pip
RUN pip install cython


RUN conda config --add channels conda-forge && \ 
    conda update -y conda 
COPY ./requirements.txt /code/requirements.txt
RUN conda install -y --file /code/requirements.txt

# lazy install
RUN conda install -y python-dotenv 
RUN pip install redis
COPY . /code/API
WORKDIR /code/API

# 
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
