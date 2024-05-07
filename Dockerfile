FROM python:3.12.3

LABEL maintainer="Darek Luczynski <rayzki@gmail.com>"

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# Bundle app source
COPY server.py itnv_pb2_grpc.py itnv_pb2.py itnv.proto /app/

EXPOSE 50053
CMD [ "python", "server.py" ]

