"""
Functions to assist with link extraction
"""

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def extract_links_by_class(base_url: str, classes: list[str]) -> list[str]:
    """
    Get a list of links from <a> elements in the response text
    where the elements have the specified classes

    Args:
        base_url:       a link to the webpage
        classes:        a list of classes to filter <a> elements

    Returns:
        full_links:     a list of links from the <a> elements

    Raises:
        ValueError:     a 4xx error while getting the link.
    """
    response: requests.Response = requests.get(base_url, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        internal_links: list[str] = soup.find_all("a", class_=" ".join(classes))
        full_links = [base_url]
        for link in internal_links:
            # Check if the link is an absolute link
            if bool(urlparse(link).netloc):
                full_links.append(link)
            else:
                full_links.append(urljoin(base_url, link))

        return full_links

    elif response.status_code in range(400, 500):
        raise ValueError(f"Bad request: received {response.status_code} for URL '{base_url}'.")
    else:
        return []
