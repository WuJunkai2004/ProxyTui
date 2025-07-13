from textual.app        import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widget     import Widget
from textual.widgets    import Button, Footer, Header, Static


from src import config

from view.overview import Form as OverviewPage
from view.proxies  import Form as ProxiesPage
from view.setting  import Form as SettingPage


class ConnectionsPage(Widget):
    """连接页面"""
    def compose(self) -> ComposeResult:
        yield Static("这里是 [bold steelblue]连接[/bold steelblue] 页面。\n\n可以实时显示当前的 TCP/UDP 连接及其路由规则。")


class LogsPage(Widget):
    """日志页面"""
    def compose(self) -> ComposeResult:
        # 将来这里可以放一个Log组件
        yield Static("这里是 [bold steelblue]日志[/bold steelblue] 页面。\n\n可以显示 Clash 内核的实时日志信息。")


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
        "config":   SettingPage,
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.now_at = config.first_page
        self.cache = {}  # 用于缓存页面实例，避免重复创建

    def compose(self) -> ComposeResult:
        """创建应用的子组件。"""
        yield Header(show_clock=True)
        
        with Horizontal(id="main-screen"):
            with VerticalScroll(id="left-pane"):
                yield Button("Overview", id="overview")
                yield Button("Proxies",  id="proxies")
                yield Button("Conns",    id="conns")
                yield Button("Logs",     id="logs")
                yield Button("Config",   id="config")
        
            # 右侧面板现在是一个空的容器，将由代码动态填充
            with VerticalScroll(id="right-pane"):
                pass
                
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        """当应用首次加载时调用，挂载默认页面。"""
        self.query_one(f"#{self.now_at}").add_class("active")
        self.switch_page(self.now_at, True)

    def switch_page(self, page_id: str, forced: bool = False) -> None:
        """切换右侧面板显示的页面。"""
        page_class = self.PAGES.get(page_id)
        if not page_class:
            return

        if page_id in self.cache:
            page_instance = self.cache[page_id]
        else:
            page_instance = page_class()
            self.cache[page_id] = page_instance
        
        if self.now_at == page_id and not forced:
            return
        self.now_at = page_id

        right_pane = self.query_one("#right-pane")
        right_pane.remove_children()
        right_pane.mount(page_instance)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """当导航按钮被按下时，切换页面。"""
        if event.button.id not in self.PAGES:
            return

        for button in self.query("#left-pane Button"):
            button.remove_class("active")
        event.button.add_class("active")

        if event.button.id:
            self.switch_page(event.button.id)



def command(cmd: str) -> int:
    pass