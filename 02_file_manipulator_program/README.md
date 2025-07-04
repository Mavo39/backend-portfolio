# File Manipulator Program

## 概要
このプログラムは、コマンドラインからファイルのコピー・反転・内容の複製・文字列置換といった基本的な操作を実行できるCLIツールです。  
OSによるファイル操作の基本を理解することを目的としています。

## 背景・目的
この課題は学習サイト「RecursionCS」で出題された演習の1つです。  
Pythonの標準ライブラリとメソッドを通じたファイル操作、およびCLIによる引数の受け渡し処理の理解を深めることを目的に取り組みました。 

## 実装機能
- ユーザーがコマンドを指定することで以下のメソッドが使用できます
1. `reverse inputpath outputpath`: inputpath にあるファイルを受け取り、outputpath に inputpath の内容を逆にした新しいファイルを作成します
2. `copy inputpath outputpath`: inputpath にあるファイルのコピーを作成し、outputpath として保存します
3. `duplicate-contents inputpath n`: inputpath にあるファイルの内容を読み込み、その内容を複製し、複製された内容を inputpath に n 回複製します
4. `replace-string inputpath needle newstring`: inputpath にあるファイルの内容から文字列 'needle' を検索し、'needle' の全てを 'newstring' に置き換えます
- 引数が正しいデータ型かどうかを判定し、検証後の引数を返す関数（文字列型・数値型）

## 工夫した点
1. 共通処理を関数化、コードの重複を削減し、保守性と可読性の向上に努めたこと
- コマンドが違っていても引数をチェックするロジックやパスが正しく存在するかどうかをチェックするロジックは同じであったため、一つの関数としてまとめました（例: validate_path()）
2. 誰が読んでも意図を理解できるような命名をしたこと
3. 関数の責務の分離を心がけたこと

## 今後の改善点
- 実装前のタスクの分解の時点で、共通化できるものと単独でしか実装できないものを明確に決めておくこと
実装し初めてから、こうした方がいい、まとめた方がいいと判断した瞬間があったので、最初の設計の段階でコードの書き直しを最小化するように、詳細を決めておくこと
- 将来的に機能が増えてきたときにはファイルをメインとモジュールなどで分けて管理すること
- 実装の順番にも気を配ること
- 大まかなものを作ってから細かく修正していくようにすること
少し初期の段階から細部にこだわっていたような感覚があったため

## 実行方法
```bash
// reverse: ファイル内容の反転
python3 file_manipulator.py reverse <inputpath> <outputpath>

// copy: ファイル内容のコピー
python3 file_manipulator.py copy <inputpath> <outputpath>

// duplicate-contents: 指定回数分内容を複製
python3 file_manipulator.py duplicate-contents <inputpath> <n>

// replace-string: 文字列の置換
python3 file_manipulator.py replace-string <inputpath> <needle> <newstring>
```

## 動作環境
- Python 3.15 以上で動作確認済み（開発時は Python 3.15.3 を使用）
- ターミナルまたはコマンドライン環境

## その他
学習記録をQiitaにまとめています(準備中)