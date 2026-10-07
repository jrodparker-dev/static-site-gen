import unittest
from split_delimiter import *
from textnode import *
from blocktypes import *

class TestSplitDelimiter(unittest.TestCase):
    def test_block_with_code(self):
        old_nodes = [TextNode("This is a text line with `some code` in it", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old_nodes, "`", TextType.CODE), 
            [ 
                TextNode("This is a text line with ", TextType.TEXT),
                TextNode("some code", TextType.CODE),
                TextNode(" in it", TextType.TEXT)  
                ])

    def test_block_with_italics(self):
        nodes = [TextNode("This is a node with an _italic_ word", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC),
            [
                TextNode("This is a node with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
                    ])
    def test_multiple_nodes(self):
        nodes = [TextNode("Phrase number one", TextType.TEXT), TextNode("Phrase number two", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD),
            [
                TextNode("Phrase number one", TextType.TEXT),
                TextNode("Phrase number two", TextType.TEXT)
            ])
    def test_bold(self):
        nodes = [TextNode("We got some **bold words out here**", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD),
            [
                TextNode("We got some ", TextType.TEXT),
                TextNode("bold words out here", TextType.BOLD)
            ])
class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_image_only(self):
        node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://example.com/image.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode(
            "Text before ![image](https://example.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://example.com/image.png",
                ),
            ],
            new_nodes,
        )

    def test_split_image_no_images(self):
        node = TextNode(
            "This is just normal text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is just normal text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_preserves_non_text_node(self):
        node = TextNode(
            "Already bold",
            TextType.BOLD,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Already bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_images_multiple_old_nodes(self):
        nodes = [
            TextNode(
                "First ![one](https://example.com/1.png)",
                TextType.TEXT,
            ),
            TextNode(
                "Second ![two](https://example.com/2.png)",
                TextType.TEXT,
            ),
        ]

        new_nodes = split_nodes_image(nodes)

        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode(
                    "one",
                    TextType.IMAGE,
                    "https://example.com/1.png",
                ),
                TextNode("Second ", TextType.TEXT),
                TextNode(
                    "two",
                    TextType.IMAGE,
                    "https://example.com/2.png",
                ),
            ],
            new_nodes,
        )
class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_split_link_only(self):
        node = TextNode(
            "[Boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode(
            "[Boot.dev](https://boot.dev) is cool",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://boot.dev",
                ),
                TextNode(" is cool", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "Go to [Boot.dev](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode(
                    "Boot.dev",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
            new_nodes,
        )

    def test_split_link_no_links(self):
        node = TextNode(
            "No links here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("No links here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_preserves_non_text_node(self):
        node = TextNode(
            "Already code",
            TextType.CODE,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Already code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_split_links_multiple_old_nodes(self):
        nodes = [
            TextNode(
                "First [one](https://one.com)",
                TextType.TEXT,
            ),
            TextNode(
                "Second [two](https://two.com)",
                TextType.TEXT,
            ),
        ]

        new_nodes = split_nodes_link(nodes)

        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode(
                    "one",
                    TextType.LINK,
                    "https://one.com",
                ),
                TextNode("Second ", TextType.TEXT),
                TextNode(
                    "two",
                    TextType.LINK,
                    "https://two.com",
                ),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = ("This is **text** with an _italic_ word and a `code block` "
        "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
        "and a [link](https://boot.dev)")
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
            TextNode(" and a ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://boot.dev",
                ),
            ],
        nodes,
    )

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )