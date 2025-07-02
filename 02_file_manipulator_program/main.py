import sys
import os

# バリデーション

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

