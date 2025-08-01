import sys
import os
import markdown

def is_markdown():
    return len(sys.argv) > 1 and sys.argv[1] == "markdown"

def is_valid_inputfile_path():
    return len(sys.argv) > 2 and os.path.exists(sys.argv[2])

def is_inputfile_markdown():
    return len(sys.argv) > 2 and sys.argv[2].strip().lower().endswith(".md")