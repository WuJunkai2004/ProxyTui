from textual.widgets import Static, Digits, Sparkline, Button
from textual.containers import Widget, Grid, Vertical
from textual.reactive import reactive


from json import loads as JSONParser



from src import lang
from src import api
from src import config


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
            yield Static(lang.get('header.title'), classes="header-title")  # 标题
            yield Button(lang.get('header.refresh'), id="refresh-button", classes="header-button")
            yield Button(lang.get('header.hide_unavailable'), id="hide-button", classes="header-button")
    
        # 代理组和节点信息
        with Grid(id="settings-grid"):
            for group in self.groups:
                with Vertical(classes="group-box"):
                    yield Static(group.name, classes="group-label")
                    yield Static(lang.get('stat.now') + str(group.now), classes="group-now")
                    for node in group.proxies:
                        if node in self.nodes:
                            node_data = self.nodes[node]
                            yield Static(node_data.name, classes="node-name")
                            yield Static(lang.get('stat.delay') + str(node_data.delay), classes="node-delay")
                        else:
                            yield Static(node, classes="node-name")
            