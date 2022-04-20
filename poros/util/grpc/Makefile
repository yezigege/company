objects = gym_pb2_grpc.py gym_pb2.py

outDir = ./gym/generate/
protoDir = ./protos

$(objects): ./protos/gym.proto
	python -m grpc_tools.protoc -I $(protoDir) --python_out=$(outDir) --grpc_python_out=$(outDir) $(protoDir)/*proto

all: $(objects)

.PHONY: clean
clean:
	cd $(outDir); rm $(objects)