"""
Inputs for testing
"""

get_page_test_cases = [
    # Basic HTML parsing test
    ("<div class='main-content'><p>Hello World</p><p>Another line</p></div>", "Hello World\nAnother line"),
    # Test with nested elements and highlight class
    ("<div class='main-content'><div class='highlight'><p>Highlighted text</p></div></div>", "Highlighted text"),
    # Test ignoring non-relevant classes
    ("<div class='sidebar'><p>Should not be included</p></div><div class='main-content'><p>Included</p></div>", "Included"),
    # Test nested div with a highlight class
    ("<div class='main-content'><div><div class='highlight'><p>Nested highlight</p></div></div></div>", "Nested highlight"),
    # Test with irrelevant content and tags
    ("<div class='main-content'><p>Main content</p><footer>Footer content</footer></div>", "Main content"),
    # Empty HTML input
    ("", ""),
    # Test multiple relevant tags
    ("<div class='main-content'><h1>Title</h1><p>Paragraph 1</p><p>Paragraph 2</p></div>", "Title\nParagraph 1\nParagraph 2"),
    # Test with no relevant content div
    ("<div class='header'><h1>Header text</h1></div><p>Orphan paragraph</p>", ""),
]


clean_text_test_cases = [
    # Test removing non-printable characters
    ("Hello\x00 World", "Hello World"),
    # Test removing consecutive duplicate lines
    ("Line 1.\nLine 2.\nLine 2.\nLine 3.", "Line 1.\nLine 2.\nLine 3."),
    # Test trimming spaces
    ("Line with spaces.     \nNext line;   ", "Line with spaces.\nNext line;"),
    # Test method signature cleanup
    ("def example_function(param): [source]\nThis is an example function.", "def example_function(param):\nThis is an example function."),
    # Test combining lines without punctuation
    ("This is a line\ncontinued here\nand then ending.", "This is a line continued here and then ending."),
    # Test ignoring line combination for specific starts
    ("This line should stay\n:rtype: int\nseparate due to rtype.", "This line should stay\n:rtype: int separate due to rtype."),
]
