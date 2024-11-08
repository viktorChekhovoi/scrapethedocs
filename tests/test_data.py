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
