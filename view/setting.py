from textual.widgets import Switch, Label, Input
from textual.containers import Widget, VerticalScroll
from textual.reactive import reactive


from src import lang
from src import api
from src import config
from src import plat


class InputBox(Widget):
    """
    一个包含标签和输入框的组件，共占两行。
    """
    # reactive 变量用于驱动UI更新
    data = reactive("")

    def __init__(self, label: str, default_value: str = "", **kwargs):
        super().__init__(**kwargs, classes="input-box")
        self.label = label
        # self.real 用于存储实际数据
        self.real = default_value

    def compose(self):
        # 布局由 .input-box 的 CSS 控制 (layout: vertical)
        yield Label(f' {self.label}', classes="box-label")
        yield Input(value=self.data, classes="box-input")

    def getData(self) -> str:
        """获取当前输入框的值。"""
        return self.real
    
    def on_mount(self):
        """挂载时，用默认值初始化 reactive 变量。"""
        self.data = self.real

    def watch_data(self, value: str) -> None:
        """当 self.data 变化时，更新 self.real。"""
        self.real = value

    def on_input_changed(self, event: Input.Changed) -> None:
        """
        【错误修正】
        当用户在输入框中键入时，此方法会被调用。
        它会更新 reactive 变量 self.data，从而触发 watch_data。
        """
        event.stop()  # 防止事件冒泡
        self.data = event.value


class SwitchBox(Widget):
    """
    一个包含标签和开关的组件，共占一行。
    """
    # reactive 变量应为布尔值以匹配 Switch 的状态
    data = reactive(False)

    def __init__(self, label: str, default_state: bool = False, **kwargs):
        super().__init__(**kwargs, classes="switch-box")
        self.label = label
        self.real = default_state

    def compose(self):
        # 布局由 .switch-box 的 CSS 控制 (layout: grid)
        yield Label(f' {self.label}', classes="box-label")
        yield Switch(value=self.data, classes="box-toggle")

    def getData(self) -> bool:
        """获取当前开关的状态。"""
        return self.real
    
    def on_mount(self):
        """挂载时，用默认值初始化 reactive 变量。"""
        self.data = self.real
    
    def watch_data(self, value: bool) -> None:
        """当 self.data 变化时，更新 self.real。"""
        self.real = value

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """
        【错误修正】
        当用户切换 Switch 时，此方法会被调用。
        它会更新 reactive 变量 self.data，从而触发 watch_data。
        """
        event.stop()  # 防止事件冒泡
        self.data = event.value


class Form(Widget):
    DEFAULT_CSS = config.style("tss/setting.css")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self):
        with VerticalScroll(id="setting-scroll"):
            yield InputBox("Clash 配置文件路径", 'config.yaml')
            yield InputBox("Clash 日志文件路径", 'clash.log')
            yield SwitchBox("启用 Clash 内核日志", True)