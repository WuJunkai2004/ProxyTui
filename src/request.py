import urllib.request as _r

def request(method, url, headers = None) -> tuple[int, str]:
    """
    Make an HTTP request.
    
    :param method: HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE')
    :param url: URL to send the request to
    :param headers: Optional dictionary of headers to include in the request
    :param data: Optional data to send with the request (for POST/PUT)
    :return: Response object
    """
    payload = headers.copy() if headers else {}
    req = _r.Request(url, headers=payload, method=method)
    with _r.urlopen(req) as response:
        status = response.getcode()
        content = response.read().decode('utf-8')
    return status, content

def stream(method, url, headers = None):
    """
    Make a streaming HTTP request and yield data line by line.

    :param method: HTTP method (e.g., 'GET')
    :param url: URL to send the request to
    :param headers: Optional dictionary of headers to include in the request
    :yield: Decoded line of response data, stripped of leading/trailing whitespace.
    """
    payload = headers.copy() if headers else {}
    req = _r.Request(url, headers=payload, method=method)
    with _r.urlopen(req) as response:
        for line in response:
            decoded_line = line.decode('utf-8').strip()
            if decoded_line:
                yield decoded_line