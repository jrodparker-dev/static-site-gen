import unittest

from block_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):

    def test_plain_paragraph(self):
        markdown = "This is a plain paragraph."

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><p>This is a plain paragraph.</p></div>"
        )

    def test_paragraph_with_bold(self):
        markdown = "This is **bold** text."

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bold</b> text.</p></div>"
        )

    def test_paragraph_with_italic(self):
        markdown = "This is _italic_ text."

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><p>This is <i>italic</i> text.</p></div>"
        )

    def test_paragraph_with_code(self):
        markdown = "This has `inline code` in it."

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><p>This has <code>inline code</code> in it.</p></div>"
        )

    def test_paragraph_with_link(self):
        markdown = "Visit [Boot.dev](https://boot.dev) today."

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            '<div><p>Visit <a href="https://boot.dev">Boot.dev</a> today.</p></div>'
        )

    def test_paragraph_with_image(self):
        markdown = "Here is ![cat](https://example.com/cat.png)."

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            '<div><p>Here is <img src="https://example.com/cat.png" alt="cat"></img>.</p></div>'
        )

    def test_paragraph_with_multiple_inline_types(self):
        markdown = (
            "This has **bold**, _italic_, `code`, "
            "[a link](https://example.com), and "
            "![an image](https://example.com/image.png)."
        )

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            '<div><p>'
            'This has <b>bold</b>, <i>italic</i>, <code>code</code>, '
            '<a href="https://example.com">a link</a>, and '
            '<img src="https://example.com/image.png" alt="an image"></img>.'
            '</p></div>'
        )

    def test_h1(self):
        markdown = "# Heading one"

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><h1>Heading one</h1></div>"
        )

    def test_h2(self):
        markdown = "## Heading two"

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><h2>Heading two</h2></div>"
        )

    def test_h6(self):
        markdown = "###### Heading six"

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><h6>Heading six</h6></div>"
        )

    def test_heading_with_inline_markdown(self):
        markdown = "### This is **very** _important_"

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><h3>This is <b>very</b> <i>important</i></h3></div>"
        )

    def test_quote_single_line(self):
        markdown = "> This is a quote"

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_quote_multiple_lines(self):
        markdown = """> This is line one
> This is line two
> This is line three"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is line one This is line two This is line three</blockquote></div>"
        )

    def test_quote_with_inline_markdown(self):
        markdown = """> This is **bold**
> and this is _italic_"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bold</b> and this is <i>italic</i></blockquote></div>"
        )

    def test_unordered_list(self):
        markdown = """- apple
- banana
- cherry"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><ul><li>apple</li><li>banana</li><li>cherry</li></ul></div>"
        )

    def test_unordered_list_with_inline_markdown(self):
        markdown = """- **bold item**
- _italic item_
- item with `code`"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><ul>"
            "<li><b>bold item</b></li>"
            "<li><i>italic item</i></li>"
            "<li>item with <code>code</code></li>"
            "</ul></div>"
        )

    def test_ordered_list(self):
        markdown = """1. first
2. second
3. third"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>"
        )

    def test_ordered_list_with_multiple_digits(self):
        markdown = """1. first
2. second
3. third
4. fourth
5. fifth
6. sixth
7. seventh
8. eighth
9. ninth
10. tenth"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><ol>"
            "<li>first</li>"
            "<li>second</li>"
            "<li>third</li>"
            "<li>fourth</li>"
            "<li>fifth</li>"
            "<li>sixth</li>"
            "<li>seventh</li>"
            "<li>eighth</li>"
            "<li>ninth</li>"
            "<li>tenth</li>"
            "</ol></div>"
        )

    def test_ordered_list_with_inline_markdown(self):
        markdown = """1. **bold**
2. _italic_
3. [link](https://example.com)"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            '<div><ol>'
            '<li><b>bold</b></li>'
            '<li><i>italic</i></li>'
            '<li><a href="https://example.com">link</a></li>'
            '</ol></div>'
        )

    def test_code_block(self):
        markdown = """```
print("hello")
print("world")
```"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            '<div><pre><code>print("hello")\nprint("world")\n</code></pre></div>'
        )

    def test_code_block_does_not_parse_inline_markdown(self):
        markdown = """```
**not bold**
_ not italic _
`not inline code`
```"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div><pre><code>**not bold**\n_ not italic _\n`not inline code`\n</code></pre></div>"
        )

    def test_multiple_blocks(self):
        markdown = """# Heading

This is a paragraph.

- one
- two

> quote"""

        html = markdown_to_html_node(markdown).to_html()

        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph.</p>"
            "<ul><li>one</li><li>two</li></ul>"
            "<blockquote>quote</blockquote>"
            "</div>"
        )