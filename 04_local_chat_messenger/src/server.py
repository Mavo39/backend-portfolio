import os
import json
import socket
from faker import Faker

config = json.load(open('config.json'))
server_address = config['udp_server_socket_filepath']

udp_server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

udp_server_socket.bind(server_address)

fake = Faker()

while True:
    print("\nwaiting to receive message ...\n")

    # リクエストデータ受け取り
    data_from_client, client_address = udp_server_socket.recvfrom(4096)
    decoded_data = data_from_client.decode('utf-8')
    print("reveived message:")
    print(f"- client address: {client_address}\n- content: {decoded_data}\n- content-size: {len(data_from_client)} bytes")

    # レスポンスデータ作成・送
    if data_from_client:
        fake_name = fake.name()
        server_sent_message = f"{fake_name} received a message '{decoded_data}'. {fake_name} is from {fake.address()}."
        server_sent_message_bytes = udp_server_socket.sendto(server_sent_message.encode('utf-8'), client_address)
        print(f"\nserver sent the below\n- content: {server_sent_message}\n- content-size: {server_sent_message_bytes} bytes")
    