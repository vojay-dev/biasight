from abc import ABC, abstractmethod

import httpx

from biasight.config import Settings


class Notifier(ABC):
    @abstractmethod
    def notify_analysis(self, uri: str, cache_hit: bool = False):
        pass


class TelegramNotifier(Notifier):
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def notify_analysis(self, uri: str, cache_hit: bool = False):
        httpx.post(
            f'https://api.telegram.org/bot{self.token}/sendMessage',
            data={'chat_id': self.chat_id, 'text': f'BiaSight analyzed {'(cache hit)' if cache_hit else ''}: {uri}'}
        )


class NoopNotifier(Notifier):
    def notify_analysis(self, uri: str, cache_hit: bool = False):
        pass


def create_notifier(settings: Settings) -> Notifier:
    if settings.telegram_enabled:
        return TelegramNotifier(settings.telegram_token, settings.telegram_chat_id)
    return NoopNotifier()
