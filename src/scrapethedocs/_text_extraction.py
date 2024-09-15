"""
Helper functions for text scraping
"""

from aiohttp import ClientSession, TCPConnector
from anyio import create_task_group
from bs4 import BeautifulSoup

from scrapethedocs._helpers import _to_sync


async def _fetch_title_async(
    session: ClientSession, link: str, results: list[tuple[str, str]]
) -> None:
    """
    Get the title of the specified URL.

    Args:
        session:    aiohttp's ClientSession
        link:       the URL to get the title from
        results:    list to contain the results

    Returns:
        None

    Raises:
        ValueError: the GET request returns any response except 200
    """
    async with session.get(link) as internal_link_response:
        if internal_link_response.status == 200:
            soup = BeautifulSoup(await internal_link_response.text(), "html.parser")
            if soup.title is None or soup.title.string is None:
                title = ""
            else:
                title = soup.title.string
            results.append((title, link))
        else:
            raise ValueError(f"Invalid link {link}, returned code {internal_link_response.status}")


@_to_sync
async def get_all_titles(links: list[str]) -> list[tuple[str, str]]:
    """
    Get the titles for all links given.

    Args:
        links:          the list of links to get titles for

    Returns:
        unique_titles:  a list of tuples (title, link) with duplicates removed
    """
    results: list[tuple[str, str]] = []
    connector = TCPConnector()
    async with ClientSession(connector=connector) as session:
        async with create_task_group() as tg:
            for link in links:
                tg.start_soon(_fetch_title_async, session, link, results)

        unique_titles = {}

        for result in results:
            if result and result[0] not in unique_titles:
                unique_titles[result[0]] = result[1]

    return list(unique_titles.values())


@_to_sync
async def get_page_text(link: str) -> str:
    """
    Get all relevant text from a URL. Code gets formatted with >>>

    Args:
        link:       the URL to the document

    Returns:
        text:       the text of the document
    """

    return link
