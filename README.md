# Introduction

myGRPC, my google Remote Procedure Call is a tryout projec to work out how the RPC for python are working.

## Local installation dependencies

``` bash
pip install grpcio grpcio-tools
```

### Generating gRPC Files

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. itnv.proto
```

### Docker operations

Dockerfile is prepared only for server. The same issue is with docker-compoese.

```bash
docker build -t mygrpc-server:1.0 .
docker run -d -p 50053:50053 mygrpc-server:1.0
docker login -u rayzki 
docker tag mygrpc-server:1.0 rayzki/mygrpc-server:1.0
docker push rayzki/mygrpc-server:1.0
```

```bash
docker compose up -d
docker compose logs -f
docker compose down
```
