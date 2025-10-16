import socket
import os

# 受付用ソケット: 接続要求を待ち受けて、新しい接続用ソケット（conn）を生成するのが唯一の役割
# 接続用ソケット: 生成された後、データの送受信という実務を担当
# データの流れ: クライアント→接続用ソケット→recv→サーバのメモリ

# サーバ内のIO操作に特化
class SocketIOHandler:
    # 接続ソケットが一度に受信するデータの最大量
    # ソケットからデータを受け取る際のパラメータのサイズをIOハンドラーで定義することで、ソケットの処理を行なうSocketIOHandlerで責任を持つ
    BUFFER_CHUNK_SIZE = 4096

    def __init__(self, socket_path):
        self.socket_path = socket_path
        # 受付用ソケットを初期化
        self.listen_socket = None

    # ソケットファイルを削除
    def _cleanup_socket_file(self):
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)

    # ソケットの初期化・起動
    def start_listening(self):
        self._cleanup_socket_file()

        # 受付用ソケットの作成・バインド・リッスン
        self.listen_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.listen_socket.bind(self.socket_path)
        self.listen_socket.listen(10)
        print(f"{self.socket_path} listening")

    # 接続の受付
    def accept_connection(self):
        # 受付用ソケットが存在しない場合
        if not self.listen_socket:
            return None

        # 受付用ソケットを使って接続用ソケットを生成
        try:
            # connection_socket: 特定のクライアントとの接続ソケット
            # TCP/IPソケットの場合、IPアドレス・ポート番号のタプルが返されるが、UNIXドメインソケットの場合返されないので、_ で無視する
            connection_socket, _ = self.listen_socket.accept()
            return connection_socket
        except OSError as e:
            print(f"Socket accept error: {e}")
            return None
        
    # 接続用ソケットからデータ受信
    def receive_data(self, connection_socket):
        return connection_socket.recv(self.BUFFER_CHUNK_SIZE)
    
    # 接続用ソケットにデータを送信
    # sendall() は、引数としてバイト列を要求する
    def send_data(self, connection_socket, data):
        connection_socket.sendall(data)

    # 受付用ソケットを閉じる
    def close(self):
        # オブジェクトが存在し、かつ有効な場合
        if self.listen_socket:
            self.listen_socket.close()
            self._cleanup_socket_file()
            print("Listen socket closed and path removed")
    