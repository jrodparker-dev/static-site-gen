from textnode import TextNode, TextType
from extraction import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        split = text.split(delimiter)
        if len(split) % 2 == 0:
            raise ValueError("Invalid Markdown syntax: unmatched delimiter")
        for i, section in enumerate(split):
            if section == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue
        current_text = node.text
        for image_alt, image_url in images:
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            current_text = sections[1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
            continue
        current_text = node.text
        for link_alt, link_url in links:
            sections = current_text.split(f"[{link_alt}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            current_text = sections[1]
    
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

