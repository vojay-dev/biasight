from datetime import date
from fastapi import HTTPException, status

class RateLimiter:

    def __init__(self, limit: int):
        self.limit = limit
        self.requests = 0
        self.last_reset = date.today()

    def check_and_update(self):
        current_date = date.today()
        if current_date > self.last_reset:
            self.requests = 0
            self.last_reset = current_date

    def increment(self):
        self.check_and_update()
        if self.requests >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Daily limit reached, please try again tomorrow"
            )
        self.requests += 1

    @property
    def usage(self):
        return self.requests

    @property
    def last_reset_iso(self):
        return self.last_reset.isoformat()
