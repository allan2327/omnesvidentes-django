FROM python:3-alpine

# Install Packages for Building Python Packages:
RUN apk add --update --virtual=.build-dependencies alpine-sdk nodejs ca-certificates musl-dev gcc python-dev make cmake g++ postgresql-dev libxml2-dev libxslt-dev

# Install Packages needed for runtime
RUN apk add --update postgresql-client git bash libxslt libxml2

# Set-up Python Environment
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt; rm requirements.txt
ADD code /code/

# Clean-up build requirements (to keep image small)
RUN apk del .build-dependencies
