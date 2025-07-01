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


# replace-string

