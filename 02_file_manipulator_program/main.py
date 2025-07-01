import sys
import os

# reverse
def reverse_file(inputpath, outputpath):
    # ファイルの読み込み
    with open(inputpath, 'r', encoding="utf-8") as f:
        contents = f.read()
    
    # ファイルに書き込み
    with open(outputpath, 'w', encoding='utf-8') as f:
        f.write(contents[::-1])
    
# copy
def copy_file(inputpath, outputpath):
    # ファイルの読み込み
    with open(inputpath, 'r', encoding='utf-8') as f:
        contents = f.read()
    
    # ファイルに書き込み
    with open(outputpath, 'w', encoding='utf-8') as f:
        f.write(contents)


# duplicate-contents


# replace-string

