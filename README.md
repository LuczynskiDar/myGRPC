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
