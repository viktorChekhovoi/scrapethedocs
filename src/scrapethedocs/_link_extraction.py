"""
Functions to assist with link extraction
"""

from urllib.parse import urljoin, urlparse

import bs4
import requests


def _get(url: str) -> requests.Response | None:
    """
    Retrieve the HTML content of a webpage and handle exceptions

    Args:
        url:            the link to the webpage

    Returns:
        response_text:  the contents of the webpage

    Raises:
        requests.exception.MissingSchema:   the URL given is invalid
        requests.exception.ConnectionError: a connection error occurred
        requests.exception.TimeoutError:    the connection timed out
    """
    try:
        response: requests.Response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as general_exception:
        print(f"A request error occurred: {general_exception}")
        return None

    if response.status_code != 200:
        print(f"The request returned a non-OK status code {response.status_code}")
        return None

    return response


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
    response = _get(base_url)
    if response is None:
        return []

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    full_links = [base_url]
    for link_element in soup.find_all("a", class_=" ".join(classes), href=True):
        link: str = link_element["href"]
        # Check if the link is an absolute link
        if bool(urlparse(link).netloc):
            full_links.append(link)
        else:
            full_links.append(urljoin(base_url, link))

    return full_links
