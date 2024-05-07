import os
import time
import grpc
from dotenv import load_dotenv
from concurrent import futures

from collections import namedtuple

import itnv_pb2
import itnv_pb2_grpc

TestElement = namedtuple("TestElement", "id, requirement, testcase")
testcases_container: list[TestElement] = []
load_dotenv()
TARGET_HOST = os.getenv('TARGET_HOST_SERVER')

def _generate_id():
    if len(testcases_container) == 0:
        id = len(testcases_container) + 1
    else:
        id = max([element.id for element in testcases_container]) + 1
    return id


def _get_id(check_id):
    if not check_id:
        id = _generate_id()
    else:
        idx = _get_idx(check_id)
        if idx:
            id = testcases_container[idx].id
        else:
            id = _generate_id()
    return id


def _get_idx(check_id):
    idxs = [idx for idx, element in enumerate(testcases_container) if element.id == check_id]
    idx = idxs[0] if idxs else None
    return idx


class Testcases(itnv_pb2_grpc.TestcasesServicer):
    def AddElement(self, request, context):
        idx = _get_idx(request.id)
        if idx:
            element = testcases_container[idx]
            element.requirement = request.requirement
            element.testcase = request.testcase
            testcases_container[idx] = element
            id = request.id
        else:
            id = _get_id(request.id)
            testcases_container.append(TestElement(id, request.requirement, request.testcase))
        print(f"Add element with Id: {request}")
        return itnv_pb2.AddResponse(id=id)

    def GetElement(self, request, context):
        idxs = self._filter_testcases_container(request)
        print(f"idxs: {idxs}")
        idx = idxs[0] if len(idxs) > 0 else None
        print(f"idx: {idx}")
        if idx is not None:
            response = testcases_container[idx]
        else:
            response = TestElement(id=-1, requirement="", testcase="")
        return itnv_pb2.GetResponse(id=response.id, requirement=response.requirement, testcase=response.testcase)

    def _filter_testcases_container(self, request):
        idxs = [idx for idx, element in enumerate(testcases_container) if element.requirement == request.requirement]
        return idxs
    
    def GetElements(self, request, context):
        idxs = self._filter_testcases_container(request)
        print(f"idxs: {idxs}")
        responses = itnv_pb2.GetResponses()
        for idx in idxs:
            item = testcases_container[idx]   
            responses.items.add(id=item.id, requirement=item.requirement, testcase=item.testcase)
        return responses

    def GetStreamedElements(self, request, context):
        idxs = self._filter_testcases_container(request)
        print(f"idxs: {idxs}")

        for idx in idxs:
            get_response = itnv_pb2.GetResponse()
            item = testcases_container[idx]   

            get_response.id = item.id
            get_response.requirement = item.requirement
            get_response.testcase = item.testcase

            yield get_response
            time.sleep(3)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    itnv_pb2_grpc.add_TestcasesServicer_to_server(Testcases(), server)
    server.add_insecure_port(TARGET_HOST)
    server.start()
    print("Server is started")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
