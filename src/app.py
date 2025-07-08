from textual.app        import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, Vertical, Grid
from textual.widget     import Widget
from textual.widgets    import Button, Footer, Header, Static, Digits, Sparkline
from textual.reactive   import reactive

import random
from collections import deque


from src import api

from view.overview import Form as OverviewPage


def get_system_stats():
    """
    获取系统状态的占位符函数。
    返回:
        一个包含上行/下行速度、内存和连接数的字典。
    """
    return {
        "upload": random.randint(50, 2048),      # 单位: KB/s
        "download": random.randint(500, 10240),  # 单位: KB/s
        "memory": random.randint(50, 150),       # 单位: MB
        "connections": random.randint(20, 200),
    }


# --- 页面组件定义 ---

class OverviewPage(Widget):
    """概览页面，包含实时统计数据和图表。"""

    DEFAULT_CSS = """
    #metrics-grid {
        grid-size: 4 1;
        grid-gutter: 1 2;
        margin-bottom: 1;
    }
    .metric-box {
        padding: 1;
        border: round $primary;
        align: center middle;
        height: 100%;
    }
    .metric-label {
        color: $text-muted;
        margin-bottom: 1;
    }
    .metric-value {
        height: 1fr;
    }
    #sparkline-container {
        padding: 1;
        border: round $primary;
    }
    .sparkline-label {
        margin-left: 2;
        margin-bottom: 1;
    }
    """

    # 为统计数据创建响应式变量
    upload = reactive(0)
    download = reactive(0)
    memory = reactive(0)
    connections = reactive(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 使用deque来存储固定长度的历史数据
        self.upload_history = deque([0.0] * 50, maxlen=50)
        self.download_history = deque([0.0] * 50, maxlen=50)

    def compose(self) -> ComposeResult:
        # 上方的四个统计数据格子
        with Grid(id="metrics-grid"):
            with Vertical(classes="metric-box"):
                yield Static("上行速度 (KB/s)", classes="metric-label")
                yield Digits(id="upload-digits", classes="metric-value")
            with Vertical(classes="metric-box"):
                yield Static("下行速度 (KB/s)", classes="metric-label")
                yield Digits(id="download-digits", classes="metric-value")
            with Vertical(classes="metric-box"):
                yield Static("内存占用 (MB)", classes="metric-label")
                yield Digits(id="memory-digits", classes="metric-value")
            with Vertical(classes="metric-box"):
                yield Static("连接数量", classes="metric-label")
                yield Digits(id="connections-digits", classes="metric-value")

        # 下方的速度历史折线图
        with Vertical(id="sparkline-container"):
            yield Static("速度历史 (KB/s)", classes="sparkline-label")
            yield Sparkline(self.upload_history, id="upload-sparkline", summary_function=max)
            yield Sparkline(self.download_history, id="download-sparkline", summary_function=max)


    def on_mount(self) -> None:
        """挂载组件后，启动一个定时器每秒更新数据。"""
        self.update_timer = self.set_interval(1, self.update_stats)




class ProxiesPage(Widget):
    """代理页面"""
    def compose(self) -> ComposeResult:
        # 将来这里可以放一个DataTable来显示所有代理
        yield Static("这里是 [bold steelblue]代理[/bold steelblue] 页面。\n\n可以显示所有代理服务器、策略组和延迟信息。")


class ConnectionsPage(Widget):
    """连接页面"""
    def compose(self) -> ComposeResult:
        yield Static("这里是 [bold steelblue]连接[/bold steelblue] 页面。\n\n可以实时显示当前的 TCP/UDP 连接及其路由规则。")


class LogsPage(Widget):
    """日志页面"""
    def compose(self) -> ComposeResult:
        # 将来这里可以放一个Log组件
        yield Static("这里是 [bold steelblue]日志[/bold steelblue] 页面。\n\n可以显示 Clash 内核的实时日志信息。")


class ConfigPage(Widget):
    """配置页面"""
    def compose(self) -> ComposeResult:
        yield Static("这里是 [bold steelblue]配置[/bold steelblue] 页面。\n\n可以用来查看和修改部分配置，例如代理模式。")


# --- 主应用 ---
class ClashUI(App):
    """一个用于Clash的Textual用户界面。"""
    CSS_PATH = "../tss/app.css" 
    BINDINGS = [
        ("q", "quit", "退出"),
    ]

    PAGES = {
        "overview": OverviewPage,
        "proxies":  ProxiesPage,
        "conns":    ConnectionsPage,
        "logs":     LogsPage,
        "config":   ConfigPage,
    }

    def compose(self) -> ComposeResult:
        """创建应用的子组件。"""
        yield Header(show_clock=True)
        
        with Horizontal(id="main-screen"):
            with VerticalScroll(id="left-pane"):
                yield Button("Overview", id="overview", classes="active")
                yield Button("Proxies",  id="proxies")
                yield Button("Conns",    id="conns")
                yield Button("Logs",     id="logs")
                yield Button("Config",   id="config")
        
            # 右侧面板现在是一个空的容器，将由代码动态填充
            with VerticalScroll(id="right-pane"):
                pass
                
        yield Footer()

    def on_mount(self) -> None:
        """当应用首次加载时调用，挂载默认页面。"""
        self.now_at = "overview"
        self.switch_page(self.now_at, True)

    def switch_page(self, page_id: str, forced: bool = False) -> None:
        """切换右侧面板显示的页面。"""
        page_class = self.PAGES.get(page_id)
        if not page_class:
            return
        
        if self.now_at == page_id and not forced:
            return
        self.now_at = page_id

        right_pane = self.query_one("#right-pane")
        right_pane.remove_children()
        right_pane.mount(page_class())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """当导航按钮被按下时，切换页面。"""
        for button in self.query("#left-pane Button"):
            button.remove_class("active")

        event.button.add_class("active")

        if event.button.id:
            self.switch_page(event.button.id)


def run():
    """运行应用。"""
    app = ClashUI()
    app.run()