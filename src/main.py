from textnode import *
import os
import shutil
from block_to_html import *

def main():
    copy_directory_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

def copy_directory_contents(source_directory, destination_directory):
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)

    os.mkdir(destination_directory)
    for item in os.listdir(source_directory):
        source_path = os.path.join(source_directory, item)
        destination_path = os.path.join(destination_directory, item)
        print(f"Copying {source_path} -> {destination_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            copy_directory_contents(source_path, destination_path)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("Not a valid title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_contents = f.read()
    with open(template_path, "r") as f:
        template_contents = f.read()
    from_html = markdown_to_html_node(from_contents).to_html()
    title = extract_title(from_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", from_html)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_contents)
    
main()