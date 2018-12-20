from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup as soup


def simple_get(url):
    """
    function makes an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('error during requests to {} : {}'.format(url, str(e)))


def is_good_response(resp):
    """
    returns true if the content html, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)


def getting_genres():
    """
    function gets genres names from main web page
    """
    url = simple_get("https://www.goodreads.com")

    if url is not None:
        html = soup(url, "html.parser")
        hit_link = [a for a in html.select('a') if a["href"].find("genres") > -1]
        if len(hit_link) > 0:
            return [a.text for a in hit_link]

    else:
        return None


def getting_new_releases(genre):
    """
    function returns new releases from genre web page
    """
    url = "https://www.goodreads.com/genres/{}"
    resp = simple_get(url.format(genre))
    
    if resp is not None:
        html = soup(resp, "html.parser")
        hit_link_div = html.findAll("div", {"class": "bigBoxBody"})[0]
        books = [img['alt'] for img in hit_link_div.select('img')]
        links = [a['href'] for a in hit_link_div.select('a')]
        return books, links

    else:
        return None


def getting_most_read(genre):
    """
    function returns most read books this week from genre web page
    """
    url = "https://www.goodreads.com/genres/most_read/{}"
    resp = simple_get(url.format(genre))
    
    if resp is not None:
        html = soup(resp, "html.parser")
        hit_link_books = html.findAll("div", {"class": "leftAlignedImage bookBox"})
        books = [img['alt'] for div in hit_link_books for img in div.select('img')]
        links = [a['href'] for div in hit_link_books for a in div.select('a')]

        return books, links

    else:
        return None


def get_info(link):
    """
    function returns rating and author for book from book web page
    """
    url = "https://www.goodreads.com{}"
    resp = simple_get(url.format(link))

    if resp is not None:
        html = soup(resp, "html.parser")
        rating = html.findAll("span", {"itemprop": "ratingValue"})[0].text.strip()
        author = html.findAll("span", {"itemprop": "name"})[0].text.strip()
        return rating, author
    else:
        return None
