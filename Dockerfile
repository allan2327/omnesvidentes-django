FROM python:3-alpine

# Install Packages for Building Python Packages:
RUN echo '@testing http://nl.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories

RUN apk add --update --virtual=.build-dependencies alpine-sdk nodejs ca-certificates musl-dev gcc python-dev make cmake g++ postgresql-dev libxml2-dev libxslt-dev
RUN apk add --update openblas-dev@testing

# Install Packages needed for runtime
RUN apk add --update postgresql-client git bash libxslt libxml2

# Set working directory for custom glibc & python setup
RUN mkdir /code
WORKDIR /code

# Additional packages for compatability (glibc)
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://raw.githubusercontent.com/sgerrand/alpine-pkg-glibc/master/sgerrand.rsa.pub && \
  wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-2.23-r3.apk && \
  wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-i18n-2.23-r3.apk && \
  wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-bin-2.23-r3.apk && \
  apk add --no-cache glibc-2.23-r3.apk glibc-bin-2.23-r3.apk glibc-i18n-2.23-r3.apk && \
  rm "/etc/apk/keys/sgerrand.rsa.pub" && \
  /usr/glibc-compat/bin/localedef --force --inputfile POSIX --charmap UTF-8 C.UTF-8 || true && \
  echo "export LANG=C.UTF-8" > /etc/profile.d/locale.sh && \
  ln -s /usr/include/locale.h /usr/include/xlocale.h

# Set-up Python Environment
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /code/
RUN pip install -r requirements.txt; rm requirements.txt
RUN python -m nltk.downloader stopwords punkt wordnet
ADD code /code/

# Clean-up build requirements (to keep image small)
RUN apk del glibc-i18n && \
  apk del .build-dependencies && \
  rm glibc-2.23-r3.apk glibc-bin-2.23-r3.apk glibc-i18n-2.23-r3.apk && \
  rm -rf /var/cache/apk/*
