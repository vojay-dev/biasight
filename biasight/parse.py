import requests
from bs4 import BeautifulSoup, Comment
import logging

logger = logging.getLogger(__name__)

MAX_CONTENT_LENGTH = 1_000_000  # 1 MB
CHUNK_SIZE = 8192  # 8 KB


def _tag_visible(element):
    if element.strip() == '':
        return False
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', 'svg', 'path', 'noscript', 'header', 'footer', 'nav', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    if element.parent.get('hidden'):
        return False
    if element.parent.get('aria-hidden') == 'true':
        return False

    return True


def _text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    texts = soup.find_all(text=True)
    visible_texts = filter(_tag_visible, texts)

    return ' '.join(t.strip() for t in visible_texts)


def parse(uri: str) -> str:
    try:
        with requests.get(uri, stream=True) as response:
            response.raise_for_status()

            content = []
            content_length = 0

            for chunk in response.iter_content(chunk_size=CHUNK_SIZE, decode_unicode=True):
                content.append(chunk)
                content_length += len(chunk)

                if content_length > MAX_CONTENT_LENGTH:
                    logger.warning('max content length %d exceeded for URI %s, truncating', MAX_CONTENT_LENGTH, uri)
                    break

            html_content = ''.join(content)
            return _text_from_html(html_content)

    except requests.RequestException as e:
        logger.error(f"Error fetching URL {uri}: {str(e)}")
        return ""
