import requests
from bs4 import BeautifulSoup, Comment
import logging

logger = logging.getLogger(__name__)

class WebParser:

    def __init__(self, max_content_length: int, chunk_size: int):
        self.max_content_length = max_content_length
        self.chunk_size = chunk_size

    @staticmethod
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

    @staticmethod
    def _text_from_html(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        texts = soup.find_all(text=True)
        visible_texts = filter(WebParser._tag_visible, texts)

        return ' '.join(t.strip() for t in visible_texts)


    def parse(self, uri: str) -> str:
        try:
            with requests.get(uri, stream=True) as response:
                response.raise_for_status()

                content = []
                content_length = 0

                for chunk in response.iter_content(chunk_size=self.chunk_size, decode_unicode=True):
                    content.append(chunk)
                    content_length += len(chunk)

                    if content_length > self.max_content_length:
                        logger.warning('max content length %d exceeded for URI %s, truncating', self.max_content_length, uri)
                        break

                html_content = ''.join(content)
                return WebParser._text_from_html(html_content)

        except requests.RequestException as e:
            logger.error(f"Error fetching URL {uri}: {str(e)}")
            return ""
