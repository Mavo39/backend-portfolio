import os
import json
import socket

config = json.load(open('config.json'))
server_address = config['udp_server_socket_filepath']
client_address = config['udp_client_socket_filepath']

udp_client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

try:
    os.unlink(client_address)
except FileNotFoundError:
    pass

udp_client_socket.bind(client_address)

with udp_client_socket:
    # リクエスト入力・送信
    message = input("Enter message: ").encode('utf-8')
    sent_message_bytes = udp_client_socket.sendto(message, server_address)
    print(f"sent content size: {sent_message_bytes} bytes")

    print("\nwaiting to receive server message ... \n")

    # レスポンス受信
    data_from_server, server_address = udp_client_socket.recvfrom(4096)
    decoded_data = data_from_server.decode('utf-8')
    print(f"received message\n- server_address: {server_address}\n- content: {decoded_data}\n- content size: {len(data_from_server)} bytes")

print("\nclosing socket\n")