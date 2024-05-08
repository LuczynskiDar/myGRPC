import os
import grpc
import argparse
import json

from dotenv import load_dotenv
from google.protobuf.json_format import MessageToJson, MessageToDict

import itnv_pb2
import itnv_pb2_grpc

load_dotenv()
TARGET_HOST = os.getenv('TARGET_HOST_CLIENT')

PROPS = ('id', 'requirement', 'testcase')
NO_ID_PROPS = ('requirement', 'testcase')

def run(**kwargs):
    with grpc.insecure_channel(target=TARGET_HOST) as channel:
        arg_values = kwargs.values()
        stub = itnv_pb2_grpc.TestcasesStub(channel=channel)
        response = None
        if all([arg is not None for arg in arg_values]):
            params = {prop: kwargs[prop] for prop in PROPS}
            id = int(params['id'])
            params['id'] = id
            response = stub.AddElement(itnv_pb2.AddRequest(**params))

        elif all([v is not None for k, v in kwargs.items() if k in NO_ID_PROPS]):
            params = {prop: kwargs[prop] for prop in NO_ID_PROPS}
            response = stub.AddElement(itnv_pb2.AddRequest(**params))
        else:
            params = {'requirement': kwargs['requirement']}
            responses = stub.GetStreamedElements(itnv_pb2.GetRequest(**params))
            
            streamed_responses = []
            for resp in responses:
                print(MessageToJson(resp, indent=4))
                streamed_responses.append(MessageToDict(resp))

            return json.dumps(streamed_responses, indent=4)
        
        if response:
            print(MessageToJson(response, indent=4))
            return MessageToJson(response, indent=4)
            


def GettingElements(params, requirement, stub):
    params = {'requirement':requirement}
    response = stub.GetStreamedElements(itnv_pb2.GetRequest(**params))
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', help='Requested id', type=str)
    parser.add_argument('-r', '--requirement', help='Requirement name', type=str)
    parser.add_argument('-t', '--testcase', help='Testcase name', type=str)
    args = parser.parse_args()
    if not args.requirement:
        raise AttributeError('The requirement attribute is missing')
    run(**vars(args))

