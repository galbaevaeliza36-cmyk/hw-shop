from django.core.cache import cache
import random

PREFIX = "confirmation_code_"
TTL = 300


def _key(email):
    return f"{PREFIX}:{email}"


def generate_confirmation_code():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))


def save_code_to_cache(email, code):
    key = _key(email)
    cache.set(key, code, TTL)


def verify_confirmation_code(email, code):
    key = _key(email)
    stored = cache.get(key)

    if stored == code:
        cache.delete(key)
        return True

    return False