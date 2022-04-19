# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
import grpc

# 支持导入新的包
import sys
sys.path.append("generate")
import generate.gym_pb2 as gym_pb2
import generate.gym_pb2_grpc as gym_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = gym_pb2_grpc.GymStub(channel)
        response = stub.BodyBuilding(gym_pb2.Person(
            name='tom', actions=['深蹲', '卧推', '硬拉']
        ))
        print(f"code: {response.code}, msg:{response.msg}")
    
if __name__ == '__main__':
    logging.basicConfig()
    run()
