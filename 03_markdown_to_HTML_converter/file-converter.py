import sys
import os
import markdown

def is_markdown():
    return len(sys.argv) > 1 and sys.argv[1] == "markdown"

def is_valid_inputfile_path():
    return len(sys.argv) > 2 and os.path.exists(sys.argv[2])

def is_inputfile_markdown():
    return len(sys.argv) > 2 and sys.argv[2].strip().lower().endswith(".md")

def outputfile_already_exists():
    return len(sys.argv) > 3 and os.path.exists(sys.argv[3])

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def write_file(path):
    with open(path, "w", encoding="utf-8") as f:
        return f.write()