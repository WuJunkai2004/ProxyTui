from textual.widgets import Static, Button, Switch, Collapsible
from textual.containers import Widget, Grid, Vertical, VerticalScroll
from textual.reactive import reactive


from json import loads as JSONParser
from base64 import b64encode


from src import lang
from src import api
from src import config


def validate(string: str) -> str:
    base = b64encode(string.encode()).decode()
    return base.replace('=', '').replace('+', '').replace('/', '')



class ProxyNode:
    def __init__(self, data):
        self.name = data['name']
        self.alive = data['alive']
        self.delay = 0
        if(self.alive and data['history']):
            self.delay = data['history'][-1]['delay']


class ProxyGroup:
    def __init__(self, data):
        self.alive = data['alive']
        self.name = data['name']
        self.now = data['now']
        self.proxies = data['all'].copy()


class ProxyWidget(Static):
    def __init__(self, node: ProxyNode):
        super().__init__(id=f'proxy-{validate(node.name)}', classes='proxy-widget')
        self.node = node
        self.update()

    def render(self):
        return f'{self.node.name} - {"Alive" if self.node.alive else "Dead"} - {self.node.delay}ms'

class Form(Widget):
    DEFAULT_CSS = config.style("tss/proxies.css")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.socket = api.API(config.URL, config.secret)
        self.groups: list[ProxyGroup]     = []
        self.nodes : dict[str, ProxyNode] = {}
        self.proxier()

    def proxier(self):
        """
        获取代理组和节点信息。
        """
        code, data = self.socket.getProxies()
        data = JSONParser(data)
        data = data['proxies']
        if code != 200:
            return
        for name in data.keys():
            if 'all' in data[name]:
                self.groups.append(ProxyGroup(data[name]))
            else:
                self.nodes[name] = ProxyNode(data[name])

    def compose(self):
        # 顶部的按钮栏
        with Grid(id="header-grid"):
            yield Button(lang.get('header.refresh'), id="refresh-button")
            yield Static(lang.get('header.hide'), id="hide-label")
            yield Switch(False, id="hide-button")
    
        # 代理组和节点信息
        with VerticalScroll(id="proxies-scroll-view"):
            for group in self.groups:
                with Collapsible(title=group.name, collapsed_symbol='', expanded_symbol='', classes='collapsible-group', id=f"group-{validate(group.name)}"):
                    with Vertical():
                        for node in group.proxies:
                            if node in self.nodes:
                                widget = ProxyWidget(self.nodes[node])
                            else:
                                widget = ProxyWidget(ProxyNode({'name': node, 'alive': False, 'history': []}))
                            yield widget
            