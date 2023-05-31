import socket
import ssl
import json
import subprocess
import time

# ===================> Client <===================

def connect_to_tls_server(
    host: str,
    port: int,
    server_cert: str,
    client_cert: str,
    client_key: str
):
    """Connect to a TLS server.

    Args:
        host (str): The server host.
        port (int): The server port.
        server_cert (str): The Server certificate.
        client_cert (str): The client certificate.
        client_key (str): The client private key.
    
    Returns:
        None
    """
    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Create an SSL context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)
    context.load_verify_locations(cafile=server_cert)

    # Wrap the socket with the SSL context -> Handshake
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname=host)
    
    # Get current IP address
    hostname = socket.gethostname()   
    ip_address = socket.gethostbyname(hostname) 

    # Send json data to the server
    data =  {
        "type": "CLIENT",
        "ip": ip_address
    }
    data = json.dumps(data)
    ssl_client_socket.send(data.encode('utf-8'))
    print(f'[+] Sent: {data}')
    
    encrypted_data = ssl_client_socket.recv(1024)
    data = encrypted_data.decode('utf-8')
    print(f'[+] Received status: {data}')
    
    # Send requested ip address to the server
    data =  {
        "ip": "sdp-gateway",
        "client_ip": ip_address,
        "port": "80",
        "protocol": "tcp",
        "timeout": "100"
    }
    data = json.dumps(data)
    ssl_client_socket.send(data.encode('utf-8'))
    print(f'[+] Sent: {data}')
    
    # Send fwknopd acces request to the gateway accross the server
    # Wait for the keys from the controller
    encrypted_data = ssl_client_socket.recv(1024)
    data = encrypted_data.decode('utf-8')
    print(f'[+] Received keys: {data}')
    
    # Wait 5 seconds to be sure that the gateway is ready
    time.sleep(5)
    subprocess.run(
        [  'fwknop', '-n', 'sdp-gateway', '-a', ip_address, '--wget-cmd', '/usr/bin/wget']
    )
    

if __name__ == '__main__':
    connect_to_tls_server(
        host='sdp-controller',
        port=5000,
        server_cert='/client/certs/controller.crt',
        client_cert='/client/certs/clients/client.crt',
        client_key='/client/certs/clients/client.key'
    )