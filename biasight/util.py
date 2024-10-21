from functools import wraps
from time import sleep
import logging

logger = logging.getLogger(__name__)

def retry(max_retries: int, ignore_exceptions: tuple = (ValueError,)) -> callable:
    def decorator(func) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not isinstance(e, ignore_exceptions):
                        logger.error(f'Error in {func.__name__}: {e}')
                        if _ < max_retries - 1:
                            logger.warning(f'Retrying {func.__name__}...')
                            sleep(1)
                        else:
                            raise e
                    else:
                        raise e

        return wrapper

    return decorator
