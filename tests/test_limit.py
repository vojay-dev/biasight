import unittest

from fastapi import HTTPException

from biasight.limit import RateLimiter


class TestRateLimiter(unittest.TestCase):

    def test_rate_limit(self):
        rate_limiter: RateLimiter = RateLimiter(2)
        rate_limiter.increment()
        self.assertEqual(1, rate_limiter.usage)

        with self.assertRaises(HTTPException):
            rate_limiter.increment()
            rate_limiter.increment()
