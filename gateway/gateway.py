import socket
import ssl
import json
import subprocess

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

    # Send json data to the server
    data =  {
        "type": "GATEWAY",
        "ip": "sdp-gateway"
    }
    data = json.dumps(data)
    ssl_client_socket.send(data.encode('utf-8'))
    print(f'[+] Sent: {data}')
    
    # Wait until the server sends data
    while True:
        
        # Receive request from the controller
        encrypted_data = ssl_client_socket.recv(1024)
        data = encrypted_data.decode('utf-8')
        data = json.loads(data)
        timeout = data['timeout'] # Get timeout from the controller in seconds
        print(f'[+] Received request: {data}')
        print("Starting fwknopd during " + str(timeout) + " seconds")
        
        # Start a process to run fwknopd and close it after timeout
        process = subprocess.Popen(["fwknopd", "-f"], stdout=subprocess.PIPE)
        
        # Send ok status to the controller
        data =  {
            "status": "OK"
        }
        data = json.dumps(data)
        ssl_client_socket.send(data.encode('utf-8'))
        
        try:
            process.wait(timeout=float(timeout))
        except subprocess.TimeoutExpired:
            print("fwknopd closed after " + str(timeout) + " seconds")
        
        
    

if __name__ == '__main__':
    connect_to_tls_server(
        host='sdp-controller',
        port=5000,
        server_cert='/gateway/certs/controller.crt',
        client_cert='/gateway/certs/clients/gateway.crt',
        client_key='/gateway/certs/clients/gateway.key'
    )