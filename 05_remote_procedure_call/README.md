# Remote Procedure Call

## 概要

このプログラムは、異なる言語間で通信を実現するリモートプロシージャコール (RPC) システムです。  
具体的には、JavaScript (Node.js) で書かれたクライアントが、Python で書かれたサーバーに対し、ネットワークを介して定義済みの関数を実行するように要求し、その結果を受け取ります。通信にはソケットを使用し、メッセージの形式には JSON を採用しています。  

このプログラムでは、同一マシン上で通信を行なう Unix ドメインソケットを使って実装しています。

## 背景・目的

このプログラムは学習サイト「RecursionCS」で出題された課題の1つです。  
異なるプログラミング言語で書かれたプログラム（クライアントとサーバー）が、共通の通信プロトコルとデータ形式（ソケットとJSON）を用いて透過的に関数を呼び出し実行できるクライアント・サーバーモデルの実装を通じて、ネットワーク通信の基本とRPCの概念の理解・習得を目的に取り組みました。  

## RPC とは
> RPC（Remote Procedure Call）とは、ネットワーク上で接続されたほかのコンピュータのプログラムを呼び出して実行させるための技術、またはそのためのプロトコルのことです。
※ https://business.ntt-west.co.jp/glossary/words-00229.html より引用

つまり、クライアントが関数を指定したリクエストをサーバに送信すると、サーバから処理結果がレスポンスとして返されます。

## リクエストとレスポンスの形式

### リクエスト

```js
{
   "method": "subtract", 
   "params": [42, 23], 
   "param_types": ["int", "int"],
   "id": 1
}
```

### レスポンス

```py
{
   "result": "19",
   "result_type": "int",
   "id": 1
}
```

## サーバによる RPC 関数の提供

サーバは、以下の関数を RPC としてクライアントに提供します。

#### 1. floor(double x)
10 進数 x を最も近い整数に切り捨て、その結果を整数で返します。

#### 2. nroot(int n, int x)
方程式 rn = x における、r の値を計算します。

#### 3. reverse(string s)
文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返します。

#### 4. validAnagram(string str1, string str2)
2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返します。

#### 5. sort(string[] strArr)
文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返します。

## 実装機能

#### クライアント(Node.js)
- 対話式 CLI インターフェース
  - readline モジュールを使用して、ユーザーからの関数名と引数の入力を対話式に受け付け
  - 利用可能な関数 (floor, nroot, reverse, validAnagram, sort) の一覧を表示し、選択を促す

- リクエストバリデーション
  - 入力された関数名が method_table に存在するかを検証する
  - 関数ごとの引数の数 (validateArgCount / sort のみ例外処理) が正しいか検証する

- 引数処理と型変換
  - 入力された引数文字列をスペースで分割し、配列化する
  - method_table に定義された param_types(double, int, string, string[]) に基づき、parseParams 関数内で適切なデータ型 (数値、文字列) に変換する。この際、厳密な型チェック（例: int 入力に小数や非数値がないか）を実施し、失敗した場合はエラーを出力して終了する

- リクエストメッセージの生成
  - 検証・変換済みのデータを用いて、指定された JSON 形式のリクエストオブジェクト (method, params, param_types, id = 1) を作成し、JSON 文字列に変換する

- ソケット通信と送受信
  - net モジュールを使用し、設定ファイルから読み込んだ RPC_SERVER_SOCKET パス (AF_UNIX ソケット) に接続  
  - JSON リクエストをサーバーに送信する(client.write(requestJSON))
  - サーバからの JSON データを受信し、パースして、結果 (result) をコンソールに出力

#### サーバー
- ソケットの初期設定と管理
  - AF_UNIX, SOCK_STREAM のソケットを作成し、設定ファイルから取得したパスにバインドする
  - 古いソケットファイルが存在する場合は削除(os.unlink)
  - `rpc_server_sock.listen(10)` でクライアントからの接続を待ち受け
  - while True ループ内で `rpc_server_sock.accept()` を呼び出し、単一のクライアント接続を受け付け

- リクエストの受信と解析
  - 接続されたソケットからデータ (`client_connection.recv(4096)`) を受信
  - 受信したバイト列を UTF-8 でデコードし、`json.loads()` で辞書にパース
  - リクエストから、method, param_types, params, id を抽出

- 関数の検索と実行
  - 抽出した method 名をキーとして、method_table.py から対応する関数オブジェクト(`method_table[method]["function"]`)を取得
  - 取得した関数をアンパックされた引数 (`*params`) と共に呼び出し、実行結果 (result) を取得
    - 提供機能: floor, nroot, reverse, validAnagram, sort

- レスポンスの作成と送信
  - 関数の実行結果 (result)、定義済みの result_type、リクエスト id を含むレスポンスオブジェクトを作成する
  - レスポンスを JSON 文字列に変換し、バイト列にエンコード
  - `client_connection.sendall()` を使ってクライアントにレスポンスを送信
  - 処理後、`client_connection.close()` で現在の接続を閉じる

## 実行方法

### ターミナル1: サーバの起動

#### 1. カレントディレクトリを server ディレクトリにする

```sh
cd src/server
```

※ ルートディレクトリからの絶対パス指定でも実行できます

#### 2. サーバ起動

```sh
python3 server.py
```

### ターミナル2: クライアントの起動とRPC実行

#### 3. カレントディレクトリの移動

```sh
cd ../../client
```

※ カレントディレクトリ server からの移動を想定

#### 4. クライアントの起動と操作

```sh
node client.js
```

- クライアント側で `node client.js` を実行後、対話式CLIに従って関数名と引数を入力してください
- 対話式CLIに順次入力
- 処理結果をサーバからレスポンスとして受信
- 処理に失敗すると、エラーメッセージを出力

#### 5. サーバを手動で終了

`Cntl` + `c` 押下

## 動作環境

Python 3.10以降

## その他

学習記録をQiitaにまとめています[Qiita記事はこちら](https://qiita.com/mabo23/items/c1b495e250a93e707a29)