FROM amd64/python:3.9-slim

# Install git
RUN apt-get -y update
RUN apt-get -y install git

# Install app dependencies
COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt && \
    apt update && apt install -y procps && rm -rf /var/lib/apt/lists/*

RUN pip3 install git+https://github.com/biomage-org/programmatic_interface

