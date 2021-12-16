from bs4 import BeautifulSoup
import os
import pytest
import requests
import time


def get_site_url():
    """
    Get url list from txt file.
    """
    current_directory = os.path.dirname(__file__)
    in_data_file = os.path.join(current_directory, 'test\\resources\\test_sitemap_in_data.txt')
    with open(in_data_file, 'r') as the_file:
        return the_file.readlines()


@pytest.fixture(scope="function")
def sitemap_urls_fixture(request):
    """
    Prepare generator, containing all urls from sitemap.xml.

    :param request: Indirect request
    """
    return get_links_generator(request.param.rstrip())


def get_links_generator(url):
    """
    Generate url list from sitemap.xml.

    :param str url: Target URL
    """
    sitemap = requests.get(''.join([url, '/sitemap.xml']))
    xml = BeautifulSoup(sitemap.text, features='html.parser')

    loc = xml.find_all('loc')

    if xml.find('urlset') is not None:
        for link in loc:
            yield link.text

    if xml.find('sitemapindex') is not None:
        for link in loc:
            yield from get_links_generator(link.text)


def get_filename(filename):
    """
    Get unique filename.

    :param str filename: filename pattern
    """
    current_directory = os.path.dirname(__file__)
    report_directory = os.path.join(current_directory, 'test\\reports\\')
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return ''.join([report_directory, filename, '_', timestamp,'.txt'])

