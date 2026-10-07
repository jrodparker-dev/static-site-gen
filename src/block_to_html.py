from split_delimiter import *
from blocktypes import *
from htmlnode import *
from textnode import *
from extraction import *


def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.paragraph:
            children = text_to_children(block)
            parent = ParentNode("p", children)
            nodes.append(parent)
        elif type == BlockType.heading:
            heading_level = 0
            for char in block:
                if char == "#":
                    heading_level += 1
                else:
                    break
            children = text_to_children(block[heading_level + 1:])
            parent = ParentNode(f"h{heading_level}", children)
            nodes.append(parent)
        elif type == BlockType.quote:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            children = text_to_children(content)
            parent = ParentNode("blockquote", children)
            nodes.append(parent)
        elif type == BlockType.unordered_list:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[2:]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            parent = ParentNode("ul", html_items)
            nodes.append(parent)
        elif type == BlockType.ordered_list:
            items = block.split("\n")
            html_items = []
            for item in items:
                parts = item.split(". ", 1)
                text = parts[1]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            parent = ParentNode("ol", html_items)
            nodes.append(parent)
        elif type == BlockType.code:
            if not block.startswith("```\n") or not block.endswith("```"):
                raise ValueError("invalid code block")

            text = block[4:-3]

            raw_text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)

            code_node = ParentNode("code", [child])
            parent = ParentNode("pre", [code_node])

            nodes.append(parent)

    return ParentNode("div", nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children