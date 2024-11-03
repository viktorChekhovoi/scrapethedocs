"""
Tests for the _link_extraction functions
"""

import requests
from pytest_mock import MockerFixture

from scrapethedocs._link_extraction import _get, extract_links_by_class


def test_get_success(mocker: MockerFixture):
    """
    Test a successful _get call
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "<html>Test Page</html>"

    mocker.patch("requests.get", return_value=mock_response)

    response = _get("https://example.com")
    assert response is not None
    assert response.status_code == 200
    assert response.text == "<html>Test Page</html>"


def test_get_request_error(mocker):
    """
    Test a _get call with a request error
    """
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException)

    response = _get("https://example.com")
    assert response is None


def test_get_non_200_status(mocker):
    """
    Test a _get call with a non-200 status
    """
    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch("requests.get", return_value=mock_response)

    response = _get("https://example.com")
    assert response is None


def test_extract_links_by_class_success(mocker):
    """
    Test successful link extraction
    """
    mock_response = mocker.Mock()
    mock_response.text = """
    <html>
        <body>
            <a href="https://example.com/page1" class="link-class">Link 1</a>
            <a href="/page2" class="link-class other-class">Link 2</a>
            <a href="/page3" class="other-class">Link 3</a>
        </body>
    </html>
    """
    mocker.patch("scrapethedocs._link_extraction._get", return_value=mock_response)

    base_url = "https://example.com"
    classes = ["link-class"]
    result = extract_links_by_class(base_url, classes)

    # Verify the result contains the expected links
    assert result == ["https://example.com", "https://example.com/page1", "https://example.com/page2"]


def test_extract_links_by_class_no_response(mocker):
    """
    Test link extraction when no HTML is found for that link
    """
    mocker.patch("scrapethedocs._link_extraction._get", return_value=None)

    base_url = "https://example.com"
    classes = ["link-class"]
    result = extract_links_by_class(base_url, classes)

    assert len(result) == 0


def test_extract_links_by_class_no_matching_links(mocker):
    """
    Test link extraction when no links match the class filter
    """
    mock_response = mocker.Mock()
    mock_response.text = """
    <html>
        <body>
            <a href="https://example.com/page1" class="other-class">Link 1</a>
            <a href="/page2" class="another-class">Link 2</a>
        </body>
    </html>
    """
    mocker.patch("scrapethedocs._link_extraction._get", return_value=mock_response)

    base_url = "https://example.com"
    classes = ["link-class"]
    result = extract_links_by_class(base_url, classes)

    assert result == ["https://example.com"]
