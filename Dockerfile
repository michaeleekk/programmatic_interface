FROM amd64/python:3.9-slim

# Install app dependencies
COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt && \
    apt update && apt install -y procps && rm -rf /var/lib/apt/lists/*

RUN pip3 install https://git+github.com/biomage-org/programmatic_interface

