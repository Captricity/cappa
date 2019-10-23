FROM ubuntu:16.04

# include cappa repo 
COPY . /cappa-master
WORKDIR /cappa-master

ARG github_token

#install dependencies
RUN apt-get update \
    && apt-get install -y \
    git \
    curl \
    ruby \
    sudo \
    software-properties-common \
    python-dev \
    python-pip \
    build-essential \
    python-setuptools \
    && curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash - \
    && apt-get install nodejs \
    && curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y yarn \
    && npm install -g bower \
    && npm install tsd@0.6.0 -g \
    && npm install -g typings \
    && gem install bundler \
    && python setup.py install \
    && bundle install \
    && add-apt-repository -y ppa:pypy/ppa \
    && apt-get -y update \
    && apt-get -y install pypy \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && pypy get-pip.py \ 
    && pip install virtualenv
