import configparser
import socket

config = configparser.ConfigParser()
config.read('config.ini')

ip_servidor = config['Cliente.ini']['ip_servidor']
puerto_servidor = config['Cliente.ini']['puerto_servidor']
ip_servidor_peer = config['Cliente.ini']['ip_servidor_peer']
puerto_servidor_peer = config['Cliente.ini']['puerto_servidor_peer']

print("IP Servidor:", type(ip_servidor))
print("Puerto Servidor:", type(puerto_servidor))
print("IP Servidor Peer:", ip_servidor_peer)
print("Puerto Servidor Peer:", puerto_servidor_peer)

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

print("IP Address:", get_ip_address())