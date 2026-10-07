from extraction import *
import unittest

class ExtractTest(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to youtube](https://youtube.com)"
        )
        self.assertListEqual([("to youtube", "https://youtube.com")], matches)
    