FROM python:3.7-slim
MAINTAINER cabreira
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
CMD gunicorn --bind 0.0.0.0:$PORT wsgi

#https://devcenter.heroku.com/articles/heroku-cli
#https://devcenter.heroku.com/articles/container-registry-and-runtime
#https://docs.docker.com/engine/install/
#https://devcenter.heroku.com/articles/container-registry-and-runtime
