"""
Tests for the _text_extraction functions
"""

from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession
from pytest_mock import MockerFixture

from scrapethedocs._text_extraction import _fetch_title_async


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
