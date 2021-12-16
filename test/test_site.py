from bs4 import BeautifulSoup
import pytest
import re
import requests

from test_sitemap.conftest import get_filename, get_site_url


@pytest.mark.parametrize("sitemap_urls_fixture", get_site_url(), indirect=True)
def test_pages_success_code(sitemap_urls_fixture):
    """
    Check links in sitemap for success response code
    """
    test_status = True
    filename = get_filename('status_code_report')

    for link in sitemap_urls_fixture:
        status_code = requests.get(link).status_code
        if re.match(r'2\d{2}', str(status_code)) is None:
            with open(filename, 'a') as out_file:
                test_status = False
                out_file.write(''.join([link, ' - ', str(status_code), '\n']))

    assert test_status, 'Some of links have status code not in 200 format'


@pytest.mark.parametrize("sitemap_urls_fixture", get_site_url(), indirect=True)
def test_selfcanonical(sitemap_urls_fixture):
    """
    Check that pages are self-referenced canonical.
    """
    test_status = True
    filename = get_filename('canonical_compare_report')

    for link in sitemap_urls_fixture:
        html = BeautifulSoup(requests.get(link).content, features='html.parser')
        try:
            canonical = html.head.find('link', attrs={'rel':'canonical'}).get('href')
        except AttributeError:
            continue
        if link != canonical:
            with open(filename, 'a') as out_file:
                test_status = False
                out_file.write(''.join([link, ' - ', canonical, '\n']))

    assert test_status, 'Some of canonical links isn\'t equal to itself address'
