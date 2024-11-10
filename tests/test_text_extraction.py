"""
Tests for the _text_extraction functions
"""

from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession
from pytest_mock import MockerFixture
from test_data import clean_text_test_cases, get_page_test_cases

from scrapethedocs._text_extraction import (
    _fetch_title_async,
    clean_page_text,
    get_all_titles,
    get_page_text,
)


@pytest.mark.asyncio
async def test_fetch_title_async_success(mocker: MockerFixture):
    """
    Test title fetching when everything works as intended
    """
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = mocker.AsyncMock(return_value="<html><head><title>Test Page</title></head></html>")

    mock_response.__aenter__.return_value = mock_response
    mock_response.__aexit__.return_value = None

    mocker.patch("aiohttp.ClientSession.get", return_value=mock_response)

    link = "https://example.com"
    results = []
    async with ClientSession() as session:
        await _fetch_title_async(session, link, results)

    assert results == [("Test Page", link)]


@pytest.mark.asyncio
async def test_fetch_title_async_no_title(mocker: MockerFixture):
    """
    Test title fetching when the page has no title
    """
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = mocker.AsyncMock(return_value="<html><head></head></html>")
    mock_response.__aenter__.return_value = mock_response
    mock_response.__aexit__.return_value = None
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_response)

    link = "https://example.com"
    results = []
    async with ClientSession() as session:
        await _fetch_title_async(session, link, results)

    assert results == [("", link)]


@pytest.mark.asyncio
async def test_fetch_title_async_non_200_status(mocker: MockerFixture):
    """
    Test title fetching when the return code is not 200
    """
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.__aenter__.return_value = mock_response
    mock_response.__aexit__.return_value = None

    mocker.patch("aiohttp.ClientSession.get", return_value=mock_response)

    link = "https://example.com"
    results = []
    async with ClientSession() as session:
        with pytest.raises(ValueError, match=f"Invalid link {link}, returned code 404"):
            await _fetch_title_async(session, link, results)

    assert len(results) == 0


def test_get_all_titles_with_valid_links(mocker: MockerFixture):
    """
    Test title fetching when all links are valid
    """
    links = ["http://example.com", "http://another.com"]
    mock_results = [("Example Title", "http://example.com"), ("Another Title", "http://another.com")]

    mocker.patch(
        "scrapethedocs._text_extraction._fetch_title_async",
        side_effect=lambda session, link, results: results.append(next((title for title in mock_results if title[1] == link), None)),
    )

    result = get_all_titles(links)

    expected_result = mock_results
    assert result == expected_result


def test_get_all_titles_with_duplicate_titles(mocker: MockerFixture):
    """
    Test duplicate filtering
    """
    links = ["http://example.com", "http://another.com", "http://example.com"]

    mock_results = [("Example Title", "http://example.com"), ("Example Title", "http://another.com")]

    mocker.patch(
        "scrapethedocs._text_extraction._fetch_title_async",
        side_effect=lambda session, link, results: results.append(next((title for title in mock_results if title[1] == link), None)),
    )

    result = get_all_titles(links)

    expected_result = [("Example Title", "http://example.com")]
    assert result == expected_result


def test_get_all_titles_with_invalid_links(mocker: MockerFixture):
    """
    Test invalid link handling
    """
    links = ["invalid_link", "http://example.com"]

    mock_results = [("Example Title", "http://example.com")]

    mocker.patch(
        "scrapethedocs._text_extraction._fetch_title_async",
        side_effect=lambda session, link, results: results.append(next((title for title in mock_results if title[1] == link), None)),
    )

    result = get_all_titles(links)

    expected_result = [("Example Title", "http://example.com")]
    assert result == expected_result


def test_get_all_titles_with_empty_links():
    """
    Test empty input
    """
    links = []

    result = get_all_titles(links)

    assert len(result) == 0


@pytest.mark.parametrize("html_input, expected_output", get_page_test_cases)
def test_get_page_text(html_input, expected_output):
    """
    Test a variety of HTML inputs
    """
    result = get_page_text(html_input)
    assert result == expected_output


@pytest.mark.parametrize("clean_input, clean_output", clean_text_test_cases)
def test_clean_page_text(clean_input, clean_output):
    """
    Test a variety of texts to clean up
    """
    result = clean_page_text(clean_input)
    assert result == clean_output
