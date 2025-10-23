import os
import socket
import json
import math

# 受付ソケットオブジェクト作成
rpc_server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

config = json.load(open('config.json'))
rpc_server_address = config['rpc_server_socket_path']

# 関数
def floor(x):
    return math.floor(x)

def nroot(n, x) -> int:
    return round(x ** (1/n))

def reverse(s):
    return s[::-1]

def validAnagram(str1, str2):
    return sorted(str1) == sorted(str2)

def sort(*strArr):
    return sorted(strArr)


# 関数一覧
method_table = {
    "floor": {
        "function": floor,
        "param_types": [ float ],
        "result_type": [ "int" ]
    }, 
    "nroot": {
        "function": nroot,
        "param_types": [ int, int ],
        "result_type": [ "int" ]
    },
    "reverse": {
        "function": reverse,
        "param_types": [ str ],
        "result_type": [ "str" ]
    },
    "validAnagram": {
        "function": validAnagram,
        "param_types": [ str, str ],
        "result_type": [ "bool" ]
    },
    "sort": {
        "function": sort,
        "param_types": [ list[str] ],  
        "result_type": [ "list[str]" ]
    }
}

try:
    os.unlink(rpc_server_address)
except FileNotFoundError:
    pass

print(f'start server on {rpc_server_address}')
print('waiting to receive a request ... \n')

# ソケットファイルをバインド
rpc_server_sock.bind(rpc_server_address)

# バックログキューの作成
rpc_server_sock.listen(10)

while True:
    client_connection, _ = rpc_server_sock.accept()

    try:
        while True:
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
                break

    finally:
        print('\nclosing current connection\n')
        client_connection.close()