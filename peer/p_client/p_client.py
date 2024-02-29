import grpc
import peer_service_pb2
import peer_service_pb2_grpc

import requests

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ip_servidor = config['Cliente.ini']['ip_servidor']
puerto_servidor = config['Cliente.ini']['puerto_servidor']
ip_servidor_peer = config['Cliente.ini']['ip_servidor_peer']
puerto_servidor_peer = config['Cliente.ini']['puerto_servidor_peer']

SERVER_URL = f"http://{ip_servidor}:{puerto_servidor}"

peer_ip = '0'

def login():
    global peer_ip
    if peer_ip != '0':
        print("Already logged in!")
        return
    username = input("Enter username: ")
    password = input("Enter password: ")
    peer_ip = input("Enter peer IP: ")

    data = {
        'username': username,
        'password': password,
        'peer_ip': peer_ip
    }
    response = requests.post(f"{SERVER_URL}/login", json=data)
    print(response.json())

def logout():
    global peer_ip
    if peer_ip != '0':
        data = {'peer_ip': peer_ip}
        response = requests.post(f"{SERVER_URL}/logout", json=data)
        print(response.json())
        peer_ip = '0'
    else:
        print("\nLogin required first!")

def index_files():
    global peer_ip
    if peer_ip != '0':
        peer_files = input("Enter peer files (comma-separated): ").split(',')
        data = {'peer_ip': peer_ip, 'peer_files': peer_files}
        response = requests.post(f"{SERVER_URL}/indexFiles", json=data)
        print(response.json())
    else:
        print("\nLogin required first!")

def get_files():
    global peer_ip
    if peer_ip != '0':
        file_name = input("Enter file name to search: ")
        data = {'file_name': file_name}
        response = requests.post(f"{SERVER_URL}/getFiles", json=data)
        peer_name = response.json()[0]['peer_name']
        print('sv_response: ', response.json())
        print('p_server response: ', download_file(peer_name, file_name), peer_ip)
        #Volver a indexar el archivo con el servidor
        data_server = {'peer_ip': peer_ip, 'peer_files': [file_name]}
        print(data_server)
        response = requests.post(f"{SERVER_URL}/indexFiles", json=data_server)
    else:
        print("\nLogin required first!")

def download_file(peer_name, file_name):
    with grpc.insecure_channel(f'{ip_servidor_peer}:{puerto_servidor_peer}') as channel:
        stub = peer_service_pb2_grpc.PeerServiceStub(channel)
        response = stub.DownloadFile(peer_service_pb2.FileRequest(peer_name=peer_name, file_name=file_name))
        return response.message

def main():
    while True:
        print("\n1. Login")
        print("2. Logout")
        print("3. Index Files")
        print("4. Get Files")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            login()
        elif choice == '2':
            logout()
        elif choice == '3':
            index_files()
        elif choice == '4':
            get_files()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
