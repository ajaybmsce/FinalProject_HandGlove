import socket
import json
import pandas

UDP_IP = "0.0.0.0"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("Running...")

with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as UDPClientSocket:
    while True:
        data, addr = sock.recvfrom(2048)
        
        json_data = json.loads(data.decode('utf-8'))
        print(json_data)
        