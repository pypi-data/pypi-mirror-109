import urllib.request as request

def get_image(url: str, filename: str):
    """Save image from URL with filename"""

    request.urlretrieve(url, filename)