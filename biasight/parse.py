import requests
from bs4 import Comment, BeautifulSoup


def _tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', 'svg', 'path', '[document]']:
        return False
    if isinstance(element, Comment):
        return False

    return True


def _text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(_tag_visible, texts)

    return u' '.join(t.strip() for t in visible_texts)


def parse(uri: str) -> str:
    response = requests.get(uri)
    return _text_from_html(response.text)
