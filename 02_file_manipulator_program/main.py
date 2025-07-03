import sys
import os

# バリデーション
## パス
def validate_path(path):
    if not os.path.exists(path):
        print(f"error: {path} does not exist.")
        sys.exit(1)

## 文字列
def validate_string(string):
    if not isinstance(string, str):
        print(f"error: '{string}' is not a string. Please procide a valid string.")
        sys.exit(1)

## 数字
def validate_int(num):
    if not isinstance(num, int):
        print(f"error: '{num}' is not an integer. Please provide a valid integer.")
        sys.exit(1)   
    elif num <= 0:
        print(f"error: {num} is not a positive integer. Please provide a valid integer.")
        sys.exit(1)

# ファイルの読み込み
def read_file(path):
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()
    
# ファイルへ書き込み
def write_file(path, contents):
    with open(path, 'w', encoding='utf-8') as f:
        return f.write(contents)

# reverse
def reverse_file(inputpath, outputpath):
    validate_path(inputpath)
    contents = read_file(inputpath)
    write_file(outputpath, contents[::-1])
    
# copy
def copy_file(inputpath, outputpath):
    validate_path(inputpath)
    contents = read_file(inputpath)
    write_file(outputpath, contents)

# duplicate-contents
def duplicate_file_contents(inputpath, n):
    validate_path(inputpath)
    validate_int(n)
    contents = read_file(inputpath)
    # ファイルの末尾に追記
    with open(inputpath, 'a', encoding='utf-8') as f:
        for i in range(n):
            f.write(contents)

# replace-string
def replace_file_string(inputpath, needle, newString):
    validate_path(inputpath)
    validate_string(needle)
    validate_string(newString)
    contents = read_file(inputpath)
    # 文字列の置換
    contents = contents.replace(needle, newString)
    # 既存ファイルに書き込み
    write_file(inputpath, contents)

