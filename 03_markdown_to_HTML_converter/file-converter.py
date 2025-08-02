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
    
def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        return f.write(content)
    
def read_markdown_file():
    if not is_valid_inputfile_path():
        print("This file does not exist.")
        sys.exit(1)

    if not is_inputfile_markdown():
        print("This file is not a markdown file.")
        sys.exit(1)
        
    return read_file(sys.argv[2])
        
def markdown_to_html(md_text):
    extensions = [
        'extra', 
        'codehilite', 
        'toc', 
        'nl2br',
    ]
    return markdown.markdown(md_text, extensions=extensions)
