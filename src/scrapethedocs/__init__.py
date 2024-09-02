#!/usr/bin/env python3

"""
Automatically collect documentation for Python packages.

This module supports the following functions:
    get_doc_home_url        Attempt to retrieve the link to a library's documentation home
                            from PyPI
    get_doc_reference_url   Attempt to retrieve the links to a library's difference guides
                            from package name or homepage link
    get_section_titles      Retrieve the titles of all sections of the documentation,
                            including nested sections
    extract_section         Retrieve all text content of a specific section
    extract_docs            Retrieve all text content of the documentation
"""

import requests
import re


def get_doc_home_url(package_name: str) -> str | None:
    """
    Get a link to library documentation from PyPI if available.

    Args:
        package_name: the name of the package as it appears on PyPI.

    Returns:
        The link to the homepage of the package's documentation website if found.
        'None' if not found.

    Raises:
        ValueError: A 4xx error while getting the link.
    """
    pypi_url = f"https://pypi.org/pypi/{package_name}/json"
    response: requests.Response = requests.get(pypi_url)
    if response.status_code == 200:
        package_info: dict = response.json()
        if not package_info or (
            "message" in package_info and package_info["message" == "Not Found"]
        ):
            return None

        urls: dict = package_info.get("info", {}).get("project_urls", {})
        docs_url = urls.get("Documentation")
        homepage_url = urls.get("Homepage")
        if docs_url:
            return docs_url
        elif homepage_url:
            return homepage_url
        else:
            return None

    elif response.status_code in range(400, 500):
        raise ValueError(
            f"Bad request: received {response.status_code} for package '{package_name}'."
        )
    else:
        return None


def get_doc_reference_url(package_url: str) -> list[str]:
    """
    Get links to the package's user guides and references if possible.

    Args:
        package_url: the link to the home page of the package's documentation

    Returns:
        A list of relevant links from that page if any are found.

    Raises:
        ValueError: A 4xx error while getting the links
    """
    response: requests.Response = requests.get(package_url)
    if response.status_code == 200:
        package_info: str = response.text
        pattern = re.compile(
            r'<a[^>]*class=["\'][^"\']*reference[^"\']*internal[^"\']*["\'][^>]*href=["\']([^"\']*)["\'][^>]*>',  # regular expression, so pylint: disable=line-too-long
            re.IGNORECASE,
        )
        matches = pattern.findall(package_info)
        full_links = [package_url]
        for match in matches:
            if re.match(r"^http", match) is not None:
                full_links.append(f"{package_url}/{match}")
            else:
                full_links.append(match)
        return full_links

    elif response.status_code in range(400, 500):
        raise ValueError(f"Bad request: received {response.status_code} for URL '{package_url}'.")
    else:
        return [package_url]


def get_section_titles(package_url: str) -> list[str]:
    """
    Get the section titles from a documentation page

    Args:
        package_url: the link to the home page of the package's documentation

    Returns:
        A list of section titles, with subsection titles formatted as
        'section/subsection/subsubsection', if any sections are found.
        None if no sections are found.


    Raises:
        ValueError: A 4xx error while getting the links
    """
    raise NotImplementedError()


def extract_section(package_url: str, section_name: str) -> str:
    """
    Get the text of a given section if it exists

    Args:
        package_url:    the link to the home page of the package's documentation
        section_name:   the name of the section, with subsection titles formatted as
                        'section/subsection/subsubsection'

    Returns:
        The text of the specified section if it exists, None otherwise


    Raises:
        ValueError: A 4xx error while getting the links
    """
    raise NotImplementedError()


def extract_docs(package_url: str) -> dict[str, str]:
    """
    Get the text of a given section if it exists

    Args:
        package_url:    the link to the home page of the package's documentation

    Returns:
        A dictionary containing the section titles as keys,
        and their text as the corresponsing value if any sections are found.
        None if no sections are found.

    Raises:
        ValueError: A 4xx error while getting the links
    """
    raise NotImplementedError()
