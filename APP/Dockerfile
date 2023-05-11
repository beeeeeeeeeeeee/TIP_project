FROM neerteam/geopandas:0.12.1
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
# RUN apk update
# RUN apk upgrade

RUN python -m pip install --upgrade pip
RUN apt-get install gcc musl-dev libffi-dev default-mysql-client -y
# move  to here to avoid re-installation of pip and apt-get
ADD requirements.txt /app/ 

#mariadb-connector-c-dev gcc musl-dev libffi-dev openssl-dev mysql-client
RUN pip install -r requirements.txt