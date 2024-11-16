"""
Tests for the main scrapethedocs functions
"""

from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture
from test_data import (
    extract_docs_test_cases,
    extract_page_test_cases,
    get_doc_home_url_test_cases,
    get_doc_reference_url_test_cases,
    get_section_titles_test_cases,
)

from scrapethedocs import (
    extract_docs,
    extract_page,
    get_doc_home_url,
    get_doc_reference_url,
    get_section_titles,
)


@pytest.mark.parametrize("package_name, mock_response, expected_url", get_doc_home_url_test_cases)
def test_get_doc_home_url(mocker: MockerFixture, package_name, mock_response, expected_url):
    """
    Test the get_doc_home_url functio on a variety of inputs
    """
    mocked_response = Mock()
    mocked_response.json.return_value = mock_response
    mock_get = mocker.patch("scrapethedocs._get", return_value=mocked_response)

    result = get_doc_home_url(package_name)

    assert result == expected_url
    mock_get.assert_called_once_with(f"https://pypi.org/pypi/{package_name}/json")


@pytest.mark.parametrize("package_url, mock_links, expected_links", get_doc_reference_url_test_cases)
def test_get_doc_reference_url(mocker, package_url, mock_links, expected_links):
    """
    Test the get_doc_reference_url function with a variety of inputs.
    """
    mock_extract_links = mocker.patch("scrapethedocs.extract_links_by_class", return_value=mock_links)

    result = get_doc_reference_url(package_url)

    assert result == expected_links
    mock_extract_links.assert_called_once_with(package_url, ["reference", "internal"])


@pytest.mark.parametrize("package_url, mock_links, mock_titles, expected_result", get_section_titles_test_cases)
def test_get_section_titles(mocker, package_url, mock_links, mock_titles, expected_result):
    """
    Test the get_section_titles function with various inputs.
    """
    mock_extract_links = mocker.patch("scrapethedocs.extract_links_by_class", return_value=mock_links)

    mock_get_all_titles = mocker.patch("scrapethedocs.get_all_titles", return_value=mock_titles)

    result = get_section_titles(package_url)

    assert result == expected_result
    mock_extract_links.assert_called_once_with(package_url, ["reference", "internal"])
    mock_get_all_titles.assert_called_once_with(mock_links)


@pytest.mark.parametrize("link, mock_response, mock_page_text, expected_result", extract_page_test_cases)
def test_extract_page(mocker, link, mock_response, mock_page_text, expected_result):
    """
    Test the extract_page function with various scenarios.
    """
    mock_get = mocker.patch("scrapethedocs._get", return_value=mock_response)

    mock_get_page_text = mocker.patch("scrapethedocs.get_page_text", return_value=mock_page_text)

    mock_clean_page_text = mocker.patch("scrapethedocs.clean_page_text", return_value=expected_result)

    result = extract_page(link)

    assert result == expected_result
    mock_get.assert_called_once_with(link)
    if mock_response:
        mock_get_page_text.assert_called_once_with(mock_response.text)
    if mock_page_text:
        mock_clean_page_text.assert_called_once_with(mock_page_text)


@pytest.mark.parametrize("package_url, mocked_titles, expected_result", extract_docs_test_cases)
def test_extract_docs(mocker, package_url, mocked_titles, expected_result):
    """
    Test the extract_docs function with various scenarios.
    """
    mock_get_section_titles = mocker.patch("scrapethedocs._link_extraction.get_section_titles", return_value=mocked_titles)

    mock_extract_page = mocker.patch(
        "scrapethedocs._link_extraction.extract_page",
        side_effect=lambda link: f"Cleaned text for {link.split('/')[-1].capitalize()}" if link != "https://docs.example.com/api" else None,
    )

    result = extract_docs(package_url)

    assert result == expected_result
    mock_get_section_titles.assert_called_once_with(package_url)
    for _, link in mocked_titles:
        mock_extract_page.assert_any_call(link)
