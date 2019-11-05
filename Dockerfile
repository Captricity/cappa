FROM ubuntu:16.04

# include cappa repo 
COPY . /cappa-master
WORKDIR /cappa-master

ARG github_token

#install dependencies
RUN apt-get update \
    && apt-get install -y \
    curl \
    sudo \
    software-properties-common \ 
    python-dev \
    python-pip \
    build-essential \
    python-setuptools \
    && curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash - \
    && curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && add-apt-repository -y ppa:pypy/ppa \
    && apt-get update \
    && apt-get install -y yarn nodejs pypy ruby git\
    && npm install -g bower tsd@0.6.0 typings \
    && python setup.py install \
    && gem install bundler \
    && bundle install \
    && pypy get-pip.py \ 
    && pip install virtualenv \
    && echo '{ "allow_root": true }' > /root/.bowerrc

