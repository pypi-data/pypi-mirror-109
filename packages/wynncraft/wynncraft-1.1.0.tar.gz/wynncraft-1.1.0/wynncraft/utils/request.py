import json
import urllib.request

from wynncraft.version import __version__
import wynncraft.utils.constants
import wynncraft.utils.rate_limiter

RateLimiter = wynncraft.utils.rate_limiter.RateLimiter()


def get(url):
    for char in url:
        if char in wynncraft.utils.constants.URL_CODES:
            url = url.replace(char, wynncraft.utils.constants.URL_CODES[char])

    if wynncraft.utils.constants.URL_V1 in url:
        url += f"&apikey={wynncraft.utils.constants.API_KEY}"
    
    req = urllib.request.Request(
        url,
        headers={
            "apikey": wynncraft.utils.constants.API_KEY,
            "User-Agent": f"wynncraft-python/{__version__}"
        }
    )
    
    RateLimiter.limit()

    res = urllib.request.urlopen(req, timeout=wynncraft.utils.constants.TIMEOUT)

    RateLimiter.update(res.info())

    return json.loads(res.read().decode("utf-8"))
