import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html(self):
        node = HTMLNode(props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        expected_repr = "HTMLNode(tag=div, value=Hello, children=[], props={'class': 'my-class'})"
        self.assertEqual(repr(node), expected_repr)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!", {"class": "my-class"})
        self.assertEqual(node.to_html(), '<div class="my-class">Hello, world!</div>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_parent_no_children(self):
        parent_node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent_node.to_html()
    