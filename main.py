#!/usr/bin/env python3

import os
import sys
from atlassian import Confluence
from dotenv import load_dotenv
import re


class InvalidConfluenceUrlException(Exception):
    pass


def print_page_content(confluence: Confluence, page_id: str):
    """
    Fetches and prints the content of a Confluence page.
    """
    try:
        page = confluence.get_page_by_id(page_id, expand='body.storage')
        content = page['body']['storage']['value']
        print(f"\n📄 Content of Page ID {page_id}:\n")
        print(content)
    except Exception as e:
        print(f"❌ Failed to fetch page content: {e}")


def add_label_to_page(confluence: Confluence, page_id: str, label: str):
    """
    Adds a label to a Confluence page.
    
    :param confluence: Authenticated Confluence object
    :param page_id: ID of the Confluence page
    :param label: Label to add
    """
    try:
        confluence.set_page_label(page_id=page_id, label=label)
        print(f"Label '{label}' added to page ID {page_id}.")
    except Exception as e:
        print(f"Failed to add label: {e}")


def is_valid_confluence_url(url: str) -> str:
    """
    Validates a Confluence URL and extracts the page ID if valid.

    :param url: The Confluence URL to validate.
    :return: True if valid, False otherwise.
    """
    pattern = r"^https://[\w\-]+\.atlassian\.net/wiki/spaces/.+/pages/(\d+)/.*$"
    match = re.match(pattern, url)
    
    if match:
        page_id = match.group(1)
        print(f"✅ Valid Confluence URL. Extracted Page ID: {page_id}")
        return page_id
    else:
        raise InvalidConfluenceUrlException("❌ Invalid Confluence URL format.")


def read_valid_lines_from_file(file_path: str, validator=None) -> list:
    """
    Reads a file line by line, applies validation, and returns valid lines as a list.

    :param file_path: Path to the file to read.
    :return: List of valid lines.
    """
    valid_lines = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                stripped_line = line.strip()
                if not stripped_line:
                    continue  # Skip empty lines
                try:
                    page_id = is_valid_confluence_url(stripped_line)
                    valid_lines.append(page_id)
                except InvalidConfluenceUrlException as e:
                    print(f"Invalid URL: {stripped_line}")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

    return valid_lines


def test_print_page_content():
    load_dotenv()

    confluence = Confluence(
        url=os.getenv("CONFLUENCE_URL"),
        username=os.getenv("CONFLUENCE_USERNAME"),
        password=os.getenv("CONFLUENCE_API_KEY")
    )

    page_id = "196845"
    print_page_content(confluence, page_id)


def test_add_label_to_page():
    load_dotenv()

    confluence = Confluence(
        url=os.getenv("CONFLUENCE_URL"),
        username=os.getenv("CONFLUENCE_USERNAME"),
        password=os.getenv("CONFLUENCE_API_KEY")
    )

    page_id = "196845"
    label = "review"
    add_label_to_page(confluence, page_id, label)

def test_is_valid_confulence_url():
    url = "https://tanishqchoudharysprinklr.atlassian.net/wiki/spaces/ENG/pages//Some-Page-Title"
    if is_valid_confluence_url(url):
        print("failed")
    else:
        print("passed")

def test_read_valid_lines_from_file():
    pass

def main():

    if len(sys.argv) < 2:
        print("❌ Please provide a URL as the first argument.")
        sys.exit(1)

    label = sys.argv[1]

    load_dotenv()

    confluence = Confluence(
        url=os.getenv("CONFLUENCE_URL"),
        username=os.getenv("CONFLUENCE_USERNAME"),
        password=os.getenv("CONFLUENCE_API_KEY")
    )

    page_id_list = read_valid_lines_from_file("urls.txt")
    for page_id in page_id_list:
        add_label_to_page(confluence, page_id, label)
        print(f"added label: {label} to page: {page_id}")


if __name__ == "__main__":
    main()
