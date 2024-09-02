"""
Functions to assist with link extraction
"""

import re
from urllib.parse import urljoin

import requests


def extract_links_by_class(base_url: str, classes: list[str]) -> list[str]:
    """
    Get a list of links from <a> elements in the response text
    where the elements have the specified classes

    Args:
        base_url: a link to the webpage
        classes: a list of classes to filter <a> elements

    Returns:
        A list of links from the <a> elements

    Raises:
        ValueError: A 4xx error while getting the link.
    """
    response: requests.Response = requests.get(base_url)
    if response.status_code == 200:
        class_patern = r'[^"\']*'.join(re.escape(html_class) for html_class in classes)
        pattern = re.compile(
            rf'<a[^>]*class=["\'][^"\']*{class_patern}[^"\']*["\'][^>]*href=["\']([^"\']*)["\'][^>]*>',  # regular expression, so pylint: disable=line-too-long
            re.IGNORECASE,
        )
        matches = pattern.findall(response.text)
        full_links = [base_url]
        for match in matches:
            if re.match(r"^http", match) is not None:
                full_links.append(urljoin(base_url, match))
            else:
                full_links.append(match)
        return full_links

    elif response.status_code in range(400, 500):
        raise ValueError(f"Bad request: received {response.status_code} for URL '{base_url}'.")
    else:
        return []
