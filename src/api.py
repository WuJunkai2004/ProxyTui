from src import request

_api_rules = {
    'getTraffic': ('GET', '/traffic'),
    'getLogs'   : ('GET', '/logs'),
    'getProxies': ('GET', '/proxies'),
    'getProxy'  : ('GET', '/proxies/{name}'),
    'setProxy'  : ('PUT', '/proxies/{name}'),
    'getDelay'  : ('GET', '/proxies/{name}/delay'),
    'getConfig' : ('GET', '/configs'),
#   'updataConfig': ('PUT', '/config'),
    'reloadConfig': ('PUT', '/configs'),
    'getRules'  : ('GET', '/rules'),
}

_keep_alive = [
    'getTraffic',
    'getLogs',
]


class API:
    __all__ = list(_api_rules.keys())
    def __init__(self, base_url, secret = None):
        """
        Initialize the Clash API client.
        :param base_url: Base URL of the Clash API (e.g., http://127.0.0.1:9090)
        :param secret: Optional secret for authentication
        """
        self.base_url = base_url
        self.headers = {}
        if secret:
            self.headers['Authorization'] = f'Bearer {secret}'

    def __getattr__(self, name):
        """
        Dynamically create methods for API endpoints based on _api_rules.
        """
        if name not in _api_rules:
            raise AttributeError(f"API method '{name}' not found.")
        
        method, path = _api_rules[name]
        
        def common_request(**kwargs):
            url = self.base_url + path.format(**kwargs)
            return request.request(method, url, headers=self.headers)
        
        def alive_request(**kwargs):
            url = self.base_url + path.format(**kwargs)
            yield from request.stream(method, url, headers=self.headers)

        if name in _keep_alive:
            return alive_request
        else:
            return common_request
    

def test():
    from src import config
    return API(config.URL, config.secret)