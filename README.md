# Introduction

myGRPC, my google Remote Procedure Call is a tryout project, to work out how the RPC for python actually works.

## Local installation dependencies

The grpc dependencies could be installed as below.

``` bash
pip install grpcio grpcio-tools
```

However the all of them are listed in requirements.txt file.

```bash
pip install -r requirements.txt
```

### Generating gRPC Files

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. itnv.proto
```

### Dotenv

Remember about creating `.env` file. Changing the `refernece.env` to `.env` might be good enough.
Pls consider to set up `.env` file ports and host per your usage.

### Docker operations

Dockerfile is prepared only for server. The same issue is with docker-compose.

To build an image and run a container pls follow as below:

```bash
docker build -t mygrpc-server:1.0 .
docker run -d -p 30353:50053 -e TARGET_HOST_SERVER='[::]:50053' mygrpc-server:1.0
```

If you prefer to use docker compose then go ahead with:

```bash
docker compose up -d
docker compose logs -f
docker compose down
```

### Docker Image publish

To publish the image on dockerhub repository, I used following:

```bash
docker login -u rayzki 
docker tag mygrpc-server:1.0 rayzki/mygrpc-server:1.0
docker push rayzki/mygrpc-server:1.0
```

Here's a link to dockerhub's [rayzki/mygrpc-server](https://hub.docker.com/r/rayzki/mygrpc-server) image

### Playing with client

The server has already implemented in-memory database, with predefined data.
From CRUD operations only Create, Read, Update are implemented. Delete operation is not implemented.

1. Create item

```bash
python client.py -i 9 -r "Security" -t "TC9"
python client.py -i 10 -r "DTC" -t "TC_DTC_10"
python client.py -r "Security" -t "TC_1"
```

As a response the item's id being received from the server

2. Update existing item

```bash
python .client.py -i 2 -r "Security" -t "TC3"
```

As a response the item's id being received from the server

3. Read data

It is allowed to read data only per `requirement` category.
Using `-i 2` or `-t "TC3"` will cause data add/update operation describe in point 1/2.

```bash
python client.py -r "Security"

```

### Logging

Logger hasn't been implemented yet to the client nor the server
