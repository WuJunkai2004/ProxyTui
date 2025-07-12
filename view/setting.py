from textual.widgets import Static, Button, Switch, Collapsible
from textual.containers import Widget, Grid, Vertical, VerticalScroll
from textual.reactive import reactive


from src import lang
from src import api
from src import config
from src import plat


class InputBox(Widget):
    DEFAULT_CSS = """
    InputBox {
        width: 100%;
        border: solid #ccc;
        height: 4;
    }
    """
    data = reactive("")
    def __init__(self, label: str, default_value: str = "", **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.real = default_value
        self.data = default_value

    def compose(self):
        with Vertical():
            yield Static(self.label, id="input-label")
            yield Static(self.data,  id="input-field")

    def getData(self):
        return self.real

    def watch_data(self, value: str) -> None:
        """
        监听输入框内容变化，更新数据。
        """
        self.real = value
        #self.query_one("#input-field").update(value)


class SwitchBox(Widget):
    DEFAULT_CSS = """
    SwitchBox {
        width: 100%;
        border: solid #ccc;
        height: 3;
    }
    .switch-box {
        display: block;
        height: auto;
    }
    """
    data = reactive(0)
    def __init__(self, label: str, default_state: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.data = default_state
        self.real = default_state

    def compose(self):
        with Grid(classes='switch-box'):
            yield Static(self.label, id="switch-label")
            yield Switch(value=self.data, id="switch-toggle")

    def getData(self):
        return self.real
    
    def watch_data(self, value: bool) -> None:
        """
        监听开关状态变化，更新数据。
        """
        self.real = value
        #self.query_one("#switch-toggle").value = value


class Form(Widget):
    #DEFAULT_CSS = config.style("tss/setting.css")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self):
        with VerticalScroll(id="setting-scroll"):
            yield InputBox("Clash 配置文件路径", 'class')
            yield InputBox("Clash 日志文件路径", 'clash.log')
            yield SwitchBox("启用 Clash 内核日志", True)