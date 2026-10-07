from enum import Enum


class BlockType(Enum):
    paragraph = 1
    heading = 2
    code = 3
    quote = 4
    unordered_list = 5
    ordered_list = 6

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()

        if block == "":
            continue

        new_blocks.append(block)
    return new_blocks


def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if (markdown.startswith("# ")
        or markdown.startswith("## ")
        or markdown.startswith("### ")
        or markdown.startswith("#### ")
        or markdown.startswith("##### ")
        or markdown.startswith("###### ")):
        return BlockType.heading
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.code
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.paragraph
        return BlockType.quote
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.unordered_list
    if all(
            line.startswith(f"{i + 1}. ")
            for i, line in enumerate(lines)
        ):
        return BlockType.ordered_list

    else:
        return BlockType.paragraph
