import grpc
import concurrent.futures
import time
import peer_service_pb2
import peer_service_pb2_grpc

import configparser
import socket

config = configparser.ConfigParser()
config.read('config.ini')
puerto = config['PServer.ini']['puerto']
sleep_time = config['PServer.ini']['sleep_time']

class PeerService(peer_service_pb2_grpc.PeerServiceServicer):
    def DownloadFile(self, request, context):
        print("200 - OK, File sent successfully!")
        return peer_service_pb2.DownloadResponse(message=f"File {request.file_name} downloaded properly!")

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    peer_service_pb2_grpc.add_PeerServiceServicer_to_server(PeerService(), server)
    server.add_insecure_port(f'[::]:{int(puerto)}')
    server.start()
    print("Server started")
    try:
        while True:
            time.sleep(int(sleep_time))
    except KeyboardInterrupt:
        server.stop(0)

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

if __name__ == '__main__':
    print("IP Address Running:", get_ip_address())
    serve()