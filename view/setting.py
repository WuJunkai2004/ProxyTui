from textual.widgets import Switch, Label, Input
from textual.containers import Widget, Vertical, VerticalScroll, Grid
from textual.reactive import reactive


from src import lang
from src import api
from src import config
from src import plat


class InputBox(Widget):
    data = reactive("")
    def __init__(self, label: str, default_value: str = "", **kwargs):
        super().__init__(**kwargs, classes="input-box")
        self.label = label
        self.real = default_value

    def compose(self):
        with Vertical():
            yield Label(self.label, classes="box-label")
            yield Input(self.data,  classes="box-input")

    def getData(self):
        return self.real
    
    def on_mount(self):
        self.data = self.real

    def watch_data(self, value: str) -> None:
        self.real = value
        #self.query_one("Input").update(value)


class SwitchBox(Widget):
    data = reactive(0)
    def __init__(self, label: str, default_state: bool = False, **kwargs):
        super().__init__(**kwargs, classes="switch-box")
        self.label = label
        self.real = default_state

    def compose(self):
        with Grid():
            yield Label (self.label,      classes="box-label")
            yield Switch(value=self.data, classes="box-toggle")

    def getData(self):
        return self.real
    
    def on_mount(self):
        self.data = self.real
    
    def watch_data(self, value: bool) -> None:
        self.real = value
        #self.query_one("Switch").value = value


class Form(Widget):
    DEFAULT_CSS = config.style("tss/setting.css")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self):
        with VerticalScroll(id="setting-scroll"):
            yield InputBox("Clash 配置文件路径", 'class')
            yield InputBox("Clash 日志文件路径", 'clash.log')
            yield SwitchBox("启用 Clash 内核日志", True)