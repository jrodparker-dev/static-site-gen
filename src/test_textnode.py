import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Hello", TextType.LINK, "https://example.com")
        node2 = TextNode("Hello", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Hello", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(Hello, 2, None)")

    def test_eq_url(self):
        node = TextNode("Hello", TextType.LINK, "https://example.com")
        node2 = TextNode("Hello", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

if __name__ == "__main__":
    unittest.main()