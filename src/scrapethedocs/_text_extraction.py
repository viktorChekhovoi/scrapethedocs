"""
Helper functions for text scraping
"""

from aiohttp import ClientSession, TCPConnector
from anyio import create_task_group
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag

from scrapethedocs._helpers import _to_sync

TEXT_ELEMENTS = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "pre"]
CONTENT_CLASSES = [
    "content",
    "main-content",
    "rst-content",
    "bd-main",
    "bd-content",
]


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
async def get_page_text(text: str) -> str:
    """
    Get all relevant text from URL contents. Code gets formatted with >>>

    Args:
        link:       the HTML contents of the document

    Returns:
        text:       the text of the document
    """
    soup = BeautifulSoup(text, "html.parser")
    lines = []
    processed_tags = set()

    def extract_text(element: PageElement) -> None:
        nonlocal lines
        nonlocal processed_tags
        if element in processed_tags:
            return

        if isinstance(element, NavigableString):
            text = element.strip()
            lines.append(text)
            processed_tags.add(element)

        elif isinstance(element, Tag):
            if element.name in TEXT_ELEMENTS:
                lines.append(element.text.strip())
                processed_tags.add(element)

            elif element.name == "div":
                classes = element.get("class", [])
                if classes is not None and "highlight" in classes:
                    lines.append(element.text.strip())
                    processed_tags.add(element)

            else:
                for child in element:
                    extract_text(child)

    def find_relevant_content(element: Tag) -> Tag | None:
        if (
            element.name == "div"
            and "class" in element.attrs
            and any(classname in element["class"] for classname in CONTENT_CLASSES)
        ):
            return element
        for child in element.findChildren(recursive=False):
            found = find_relevant_content(child)
            if found is not None:
                return found
        return None

    content_div = find_relevant_content(soup)
    if content_div is not None:
        extract_text(content_div)

    lines = [line for line in lines if len(line) > 0]
    return "\n".join(lines)
