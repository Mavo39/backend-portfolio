import os
import socket
import json
import sys
from method_table import method_table
from pathlib import Path

# 受付ソケットオブジェクト作成
rpc_server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

root_dir = Path(__file__).parent.parent.parent
config_path = root_dir / 'config.json'

# 設定ファイルのロード
try:
    with open(config_path) as config_file:
        config = json.load(config_file)

except FileNotFoundError:
    print(f'エラー: 設定ファイルが見つかりませんでした\n{config_path}')
    sys.exit(1)

# /tmp/server.sockを設定
rpc_server_address = config['rpc_server_socket_path']

# 旧受付ソケットファイルの削除
try:
    os.unlink(rpc_server_address)
except FileNotFoundError:
    pass

print(f'start server on {rpc_server_address}')

# ソケットファイルをバインド
rpc_server_sock.bind(rpc_server_address)

# バックログキューの作成
rpc_server_sock.listen(10)

def send_error_response(connection, message, request_id):
    error_response = {
        "error_message": message,
        "request_id": request_id
    }
    errorJSON = json.dumps(error_response)
    connection.sendall(errorJSON.encode('utf-8'))

while True:
    print('waiting to receive a request ... \n')
    client_connection, _ = rpc_server_sock.accept()

    if input() == "exit":
        client_connection.close()
        break

    try:
        data = client_connection.recv(4096)
        request_dict = json.loads(data)

        if request_dict:
            print(f'received request: {request_dict}')

            method = request_dict['method']
            param_types = request_dict['param_types']
            params = request_dict['params']
            request_id = request_dict['id']
            
            # 関数の取り出し
            res = method_table[method]["function"]

            # 引数のデータ型検証
            for i in range(len(params)):
                # string[]の場合: 引数が str 型かどうかを一つずつチェック
                if param_types[0] == "string[]":
                    for j in range(len(params)):
                        if type(params[j]) != str:
                            print("data type is not correct")
                # その他
                elif type(params[i]) != method_table[method]["param_types"][i]:
                    print("data type is not correct")

            # 関数実行
            result = res(*params)

            # レスポンス作成
            response = {
                "result": result,
                "result_type": method_table[method]["result_type"],
                "id": request_id
            }

            # レスポンスのJSON化
            responseJSON = json.dumps(response)
            print(f'sending response: {responseJSON}')
            
            # JSONレスポンスのバイト列化
            byte_responseJSON = responseJSON.encode('utf-8')

            # レスポンスの送信
            client_connection.sendall(byte_responseJSON)

    finally:
        print('\nclosing current connection\n')
        client_connection.close()