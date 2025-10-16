import json

# リクエストハンドラーを担当するクラス

class RpcServer:
    # 依存性の注入を使用して、処理を他クラスに委譲
    def __init__(self, socket_io_handler, rpc_service, response_builder):
        self.socket_io_handler = socket_io_handler
        self.rpc_service = rpc_service
        self.response_builder = response_builder

    # サーバの起動・メインループの開始
    def start(self):
        # 受付用ソケットの起動
        self.socket_io_handler.start_listening()

        try:
            while True:
                # 接続ソケットを都度生成
                connection_socket = self.socket_io_handler.accept_connection()

                if connection_socket:
                    self._handle_connection(connection_socket)
        except Exception as e:
            print(f"\nfatal server error: {e}")
        finally:
            self.socket_io_handler.close()

    # 接続用ソケットからデータ受信
    def _receive_full_message(self, connection_socket):
        full_data = b''
        while True:
            # 1回あたり4096バイトのデータを受信
            # data バイト列を受信する
            data = self.socket_io_handler.receive_data(connection_socket)
            if not data:
                return ""
            full_data += data
            decorded_data = full_data.decode('utf-8')
            return decorded_data
        
    # レスポンス文字列を送信
    def _send_full_message(self, connection_socket, data_str):
        send_data = data_str.encode('utf-8')
        self.socket_io_handler.send_data(connection_socket, send_data)

    # 接続用ソケットを使った通信
    def _handle_connection(self, connection_socket):
        # リクエストの受信・デコード

        # 処理の委譲(詳細はrpc_serviceで実装)

        # レスポンス生成(詳細はresponse_builderで実装)

        # レスポンスの送信
        
        return