from flask import Flask, request, jsonify
import json
import configparser

app = Flask(__name__)
LOGGED_PEERS_FILE = "logged_peers.json"

def load_logged_peers():
    try:
        with open(LOGGED_PEERS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    peer_ip = data.get('peer_ip')
    logged_peer = {username: peer_ip}
    write_logged_peer(logged_peer)
    return jsonify({
        'username': username,
        'password': password,
        'peer_ip': peer_ip
    })

@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    peer_ip = data.get('peer_ip')
    remove_logged_peer(peer_ip)
    return jsonify({'message': f'Logged out peer with IP {peer_ip}'}), 200

@app.route('/indexFiles', methods=['POST'])
def index_files():
    logged_peers = load_logged_peers()
    data = request.json
    peer_ip = data.get('peer_ip')
    peer_files = data.get('peer_files')
    peer_name = None
    for name, info in logged_peers.items():
        if peer_ip in info: 
            peer_name = name
            break
    if peer_name is None:
        return jsonify({'error': 'Peer IP not found.'}), 404
    
    logged_peers[peer_name][1].extend(peer_files)
    with open(LOGGED_PEERS_FILE, 'w') as file:
        json.dump(logged_peers, file, indent=4)
    return jsonify({'message': 'Files indexed successfully.'}), 200

@app.route('/getFiles', methods=['POST'])
def get_files():
    logged_peers = load_logged_peers()  
    data = request.json
    file_name = data.get('file_name')
    matching_files = [] 
    for peer_name, peer_info in logged_peers.items():
        if file_name in peer_info[1]:
            peer_ip = peer_info[0]
            download_link = f'http://{peer_ip}/download/{peer_name}/{file_name}'
            matching_files.append({'peer_name': peer_name, 'peer_ip': peer_ip, 'file_name': file_name, 'download_link': download_link})
    if matching_files:
        return jsonify(matching_files)
    else:
        return jsonify({'message': 'File not found.'}), 404



def write_logged_peer(logged_peer):
    logged_peers = load_logged_peers() 
    for peer_name, peer_ip in logged_peer.items():
        if peer_name in logged_peers:
            logged_peers[peer_name].append([peer_ip, [0]])  
        else:
            logged_peers[peer_name] = [peer_ip, [0]] 
    with open(LOGGED_PEERS_FILE, 'w') as file:
        json.dump(logged_peers, file, indent=4)

def remove_logged_peer(peer_ip):
    logged_peers = load_logged_peers()  
    keys_to_delete = []
    for peer_name, ip_list in logged_peers.items():
        if peer_ip in ip_list:
            del logged_peers[peer_name]
            break 
    with open(LOGGED_PEERS_FILE, 'w') as file:
        json.dump(logged_peers, file, indent=4)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = config['Servidor.ini']['ip']
    port = config['Servidor.ini']['puerto']
    app.run(host=host, debug=True, port=int(port))
