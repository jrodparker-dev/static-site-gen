import unittest
from blocktypes import *
from block_to_html import *

class TestBlockLogic(unittest.TestCase):
    def test_heading_block(self):
        markdown = "### This is a heading"
        self.assertEqual(block_to_block_type(markdown), BlockType.heading)
    def test_code_block(self):
        markdown = """```python
        print('hello')
        print('world')
        ```"""
        self.assertEqual(block_to_block_type(markdown), BlockType.code)