"""
Inputs for testing
"""

from unittest.mock import Mock

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


get_doc_home_url_test_cases = [
    # Test when "Documentation" URL is available
    (
        "test_package",
        {
            "info": {
                "project_urls": {
                    "Documentation": "https://docs.example.com",
                    "Homepage": "https://homepage.example.com",
                }
            }
        },
        "https://docs.example.com",
    ),
    # Test when only "Homepage" URL is available
    (
        "test_package",
        {
            "info": {
                "project_urls": {
                    "Homepage": "https://homepage.example.com",
                }
            }
        },
        "https://homepage.example.com",
    ),
    # Test when no URLs are available
    (
        "test_package",
        {"info": {"project_urls": {}}},
        None,
    ),
    # Test when response is None (e.g., no response from _get)
    ("test_package", None, None),
    # Test when package not found
    ("nonexistent_package", {"message": "Not Found"}, None),
    # Test when unexpected response structure is returned
    ("test_package", {}, None),
]


get_doc_reference_url_test_cases = [
    # Case: No links are found on the page, return the original package URL
    ("https://docs.example.com", [], ["https://docs.example.com"]),
    # Case: Links are found on the page
    (
        "https://docs.example.com",
        ["https://docs.example.com/ref1", "https://docs.example.com/ref2"],
        ["https://docs.example.com/ref1", "https://docs.example.com/ref2"],
    ),
]


get_section_titles_test_cases = [
    # Case: No links are found; return an empty list
    ("https://docs.example.com", [], [], []),
    # Case: Links are found, and get_all_titles processes them
    (
        "https://docs.example.com",
        ["https://docs.example.com/section1", "https://docs.example.com/section2"],
        [("Section 1", "https://docs.example.com/section1"), ("Section 2", "https://docs.example.com/section2")],
        [("Section 1", "https://docs.example.com/section1"), ("Section 2", "https://docs.example.com/section2")],
    ),
]


extract_page_test_cases = [
    # Case: _get returns None; function should return None
    ("https://docs.example.com", None, None, None),
    # Case: _get returns a response, and get_page_text and clean_page_text process it
    (
        "https://docs.example.com",
        Mock(text="Raw HTML content"),
        "Extracted page text",
        "Cleaned page text",
    ),
    # Case: _get returns a response, but get_page_text returns an empty string
    (
        "https://docs.example.com",
        Mock(text="Another raw HTML content"),
        "",
        "",
    ),
]


extract_docs_test_cases = [
    # Case: No sections found (get_section_titles returns an empty list)
    (
        "https://docs.example.com",
        [],  # Mocked section titles
        {},  # Expected result
    ),
    # Case: One section found and processed successfully
    (
        "https://docs.example.com",
        [("Introduction", "https://docs.example.com/intro")],  # Mocked section titles
        {"Introduction": "Cleaned text for Introduction"},  # Expected result
    ),
    # Case: Multiple sections found and processed
    (
        "https://docs.example.com",
        [
            ("Introduction", "https://docs.example.com/intro"),
            ("Usage Guide", "https://docs.example.com/usage"),
        ],  # Mocked section titles
        {
            "Introduction": "Cleaned text for Introduction",
            "Usage Guide": "Cleaned text for Usage Guide",
        },  # Expected result
    ),
    # Case: Section link fails to extract page (extract_page returns None)
    (
        "https://docs.example.com",
        [
            ("Introduction", "https://docs.example.com/intro"),
            ("API Reference", "https://docs.example.com/api"),
        ],  # Mocked section titles
        {
            "Introduction": "Cleaned text for Introduction",
            "API Reference": None,
        },  # Expected result
    ),
]
