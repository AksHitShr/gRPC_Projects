import grpc
from concurrent import futures
import knn_pb2
import knn_pb2_grpc
import numpy as np
import sys

class KNNService(knn_pb2_grpc.KNNServiceServicer):
    def __init__(self, dataset):
        self.dataset = dataset

    def FindKNearestNeighbors(self, request, context):
        print(f"Received query point and k: {request}")
        query_point = np.array(request.data_point)
        k = request.k
        distances = []
        for data_point in self.dataset:
            distance = np.linalg.norm(np.array(data_point) - query_point)
            distances.append((data_point, distance))
        # Sort based on distance and select k-nearest neighbors
        distances.sort(key=lambda x: x[1])
        num = min(len(self.dataset),k)
        k_nearest_neighbors = distances[:num]

        # Create the response
        response = knn_pb2.KNNResponse()
        for neighbor, distance in k_nearest_neighbors:
            response.neighbors.add(point=neighbor, distance=distance)
        
        return response

def serve(port, dataset_file):
    dataset = np.loadtxt(dataset_file, delimiter=',')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    knn_pb2_grpc.add_KNNServiceServicer_to_server(KNNService(dataset), server)
    server.add_insecure_port(f'[::]:{port}')
    print(f'Server started on port {port}, using dataset {dataset_file}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python server.py <port> <dataset_file>")
        sys.exit(1)

    port = sys.argv[1]
    dataset_file = sys.argv[2]
    serve(port, dataset_file)
