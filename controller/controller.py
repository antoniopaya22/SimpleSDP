import socket
import ssl
import json


# ===================> Server <===================

open_sockets = []
gateways = {}
clients = {}

def start_tls_server(key: str, cert: str, clients_folder: str, port: int, host: str):
    """"
    Starts a TLS server on the given port and host.
    
    Args:
        key (str): The server's private key file.
        cert (str): The server's certificate file.
        clients_folder (str): The client's certificates folder.
        port (int): The server's port.
        host (str): The server's host.
        
    Returns:
        None
    """
    # Create a socket and bind it to the host and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # Create an SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert, keyfile=key)
    # Verify client certificates
    context.load_verify_locations(capath=clients_folder)
    # Listen for incoming connections
    server_socket.listen(1)
    print(f'[+] Listening on {host}:{port}...')
    
    # Handle clients
    while True:    
        # Accept the connection
        client_socket, client_address = server_socket.accept()
        print(f'[+] Accepted connection from {client_address[0]}:{client_address[1]}')
        # Perform SSL handshake
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        print(f'[+] SSL established. Peer: {ssl_socket.getpeercert()}')
        open_sockets.append(ssl_socket)
        # Handle the client in a new thread
        from threading import Thread
        thread = Thread(target=handle_client, args=(ssl_socket, context))
        thread.start()
    

def handle_client(client_socket: ssl.SSLSocket, context: ssl.SSLContext):
    """Handle a client connection.

    Args:
        client_socket (ssl.SSLSocket): The client socket.

    Returns:
        None
    """
    
    # Receive data from the client
    encrypted_data = client_socket.recv(1024)
    data = encrypted_data.decode('utf-8')
    print(f'[+] Received: {data}')
    
    # Check if the client is a GATEWAY or a CLIENT
    json_data = json.loads(data)
    client_type = json_data['type']
    ip = json_data['ip']
    
    if client_type == "GATEWAY":
        gateways[ip] = client_socket
        print(f'[+] Gateway {ip} connected.')
        
    elif client_type == "CLIENT":
        clients[ip] = client_socket
        print(f'[+] Client {ip} connected.')
        
        # Send ok to the client
        data = {
            "status": "OK"
        }
        data = json.dumps(data)
        client_socket.send(data.encode('utf-8'))
        
        # Get clients access request
        access_data = client_socket.recv(1024)
        data = json.loads(access_data.decode('utf-8'))
        ip = data['ip']
        client_ip = data['client_ip']
        port = data['port']
        protocol = data['protocol']
        timeout = data['timeout']
        print(f'[+] Client {ip} requested access to {client_ip}:{port} ({protocol})')
        # Start the gateway fwknop server
        data = json.dumps(data)
        gateway_socket = gateways[ip]
        gateway_socket.send(data.encode('utf-8'))
        # Get the gateway's response
        encrypted_data = gateway_socket.recv(1024)
        data = encrypted_data.decode('utf-8')
        data = json.loads(data)
        print(f'[+] Received from gateway: {data}')
        # Send keys to the client
        keys = "abc"
        data = {
            keys: keys
        }
        data = json.dumps(data)
        client_socket.send(data.encode('utf-8'))


if __name__ == '__main__':
    # Server's host and port
    HOST = '0.0.0.0'
    PORT = 5000
    # Server's certificate and private key files
    CERT_FILE = '/controller/certs/controller.crt'
    KEY_FILE = '/controller/certs/controller.key'
    CLIENTS_FOLDER = '/controller/certs/clients/'
    start_tls_server(KEY_FILE, CERT_FILE, CLIENTS_FOLDER, PORT, HOST)