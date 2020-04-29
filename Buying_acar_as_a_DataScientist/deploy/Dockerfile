FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++
RUN pip3 install -r requirements.txt
RUN python db_starter.py

CMD gunicorn --bind 0.0.0.0:$PORT wsgi


#https://cabreirajm.herokuapp.com/ 
