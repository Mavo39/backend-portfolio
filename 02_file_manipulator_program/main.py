import sys
import os

# バリデーション
## パス
def validate_path(path):
    return os.path.exists(path)

## 文字列
def is_string(string):
    return isinstance(string, str)

## 数字
def is_int(num):
    return isinstance(num, int)

# ファイルの読み込み
def read_file(inputpath):
    with open(inputpath, 'r', encoding="utf-8") as f:
        return f.read()

# reverse
def reverse_file(inputpath, outputpath):
    contents = read_file(inputpath)
    
    # ファイルに書き込み
    with open(outputpath, 'w', encoding='utf-8') as f:
        f.write(contents[::-1])
    
# copy
def copy_file(inputpath, outputpath):
    contents = read_file(inputpath)
    
    # ファイルに書き込み
    with open(outputpath, 'w', encoding='utf-8') as f:
        f.write(contents)


# duplicate-contents
def duplicate_file_contents(inputpath, n):
    # n のバリデーションチェック（後ほど実装）

    # ファイルの読み込み
    contents = read_file(inputpath)

    # ファイルの末尾に追記
    with open(inputpath, 'a', encoding='utf-8') as f:
        for i in range(n):
            f.write(contents)

# replace-string
def replace_file_string(inputpath, needle, newString):
    # 文字列とファイルパスのバリデーション（後ほど追加）

    # ファイルの読み込み
    contents = read_file(inputpath)

    # 文字列の置換
    contents = contents.replace(needle, newString)

    # 既存ファイルに書き込み
    with open(inputpath, 'w', encoding='utf-8') as f:
        f.write(contents)
