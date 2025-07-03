import sys
import os

# バリデーション
## パス
def validate_path(path):
    abs_path = os.path.abspath(path)

    if not os.path.exists(abs_path):
        print(f"error: {abs_path} does not exist.")
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

def main():
    if len(sys.argv) < 2:
        print("error: No specified command.")
        sys.exit(1)

    command = sys.argv[1]
    validate_string(command)

    if command == "reverse":
        if len(sys.argv) != 4:
            print("error: 'reverse' requires 2 arguments")
            sys.exit(1)
        reverse_file(sys.argv[2], sys.argv[3])

    elif command == "copy":
        if len(sys.argv) != 4:
            print("error: 'copy' requires 2 arguments")
            sys.exit(1)
        copy_file(sys.argv[2], sys.argv[3])

    elif command == "duplicate-contents":
        if len(sys.argv) != 4:
            print("error: 'duplicate-contents' requires 2 arguments")
            sys.exit(1)
        duplicate_file_contents(sys.argv[2], sys.argv[3])

    elif command == "replace-string":
        if len(sys.argv) != 5:
            print("error: 'replace-string' requires 3 arguments")
            sys.exit(1)
        replace_file_string(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        print(f"error: '{command}' is not defined.")
        sys.exit(1)

if __name__ == "__main__":
    main()