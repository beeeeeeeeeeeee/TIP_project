
FROM nickgryg/alpine-pandas
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN apk add mariadb-connector-c-dev gcc musl-dev libffi-dev openssl-dev mysql-client
RUN pip install -r requirements.txt
ADD . .