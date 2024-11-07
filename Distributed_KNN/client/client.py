import grpc
import knn_pb2
import knn_pb2_grpc
import numpy as np
import heapq
from threading import Thread, Lock
import time

mutex = Lock()

def get_knn_from_server(server_address, query_point, k):
    with grpc.insecure_channel(server_address) as channel:
        stub = knn_pb2_grpc.KNNServiceStub(channel)
        request = knn_pb2.KNNRequest(data_point=query_point, k=k)
        response = stub.FindKNearestNeighbors(request)
    return [(list(neighbor.point), neighbor.distance) for neighbor in response.neighbors]

def aggregate_knn(all_neighbors, k):
    # Use a max-heap to keep track of the global k-nearest neighbors
    heap = []
    for neighbors in all_neighbors:
        for neighbor, distance in neighbors:
            if len(heap) < k:
                heapq.heappush(heap, (-distance, neighbor))
            else:
                if -heap[0][0] > distance:
                    heapq.heappop(heap)
                    heapq.heappush(heap, (-distance, neighbor))
    # Return the k-nearest neighbors sorted by distance
    return sorted([(-dist, point) for dist, point in heap])

def query_servers(servers, query_point, k):
    all_neighbors = []
    threads = []
    def query_server(server):
        neighbors = get_knn_from_server(server, query_point, k)
        with mutex:
            all_neighbors.append(neighbors)
    # Query each server in parallel
    for server in servers:
        thread = Thread(target=query_server, args=(server,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return aggregate_knn(all_neighbors, k)

if __name__ == '__main__':
    t1=time.time()
    servers = ['localhost:50051', 'localhost:50052']
    # Query point
    query_point = np.array([2.0, 1.0, 4.0])
    k = 2
    global_knn = query_servers(servers, query_point, k)
    t2=time.time()
    print(f"Time Taken: {t2-t1}")
    print('Global k-nearest neighbors:')
    for distance, neighbor in global_knn:
        print(f'Point: {neighbor}, Distance: {distance}')
