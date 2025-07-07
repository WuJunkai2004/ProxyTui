from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widget import Widget
from textual.widgets import Button, Footer, Header, Static

# --- 页面组件定义 ---
# 每个页面都是一个独立的Widget类，可以包含自己的布局、组件和逻辑

class OverviewPage(Widget):
    """概览页面"""
    def compose(self) -> ComposeResult:
        yield Static("这里是 [bold steelblue]概览[/bold steelblue] 页面。\n\n可以显示一些汇总信息，例如上行/下行速度。")

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

    # 将按钮ID映射到对应的页面类
    PAGES = {
        "overview": OverviewPage,
        "proxies": ProxiesPage,
        "conns": ConnectionsPage,
        "logs": LogsPage,
        "config": ConfigPage,
    }

    def compose(self) -> ComposeResult:
        """创建应用的子组件。"""
        yield Header(show_clock=True)
        
        with Horizontal(id="main-screen"):
            with VerticalScroll(id="left-pane"):
                yield Button("概览 (Overview)", id="overview", classes="active")
                yield Button("代理 (Proxies)", id="proxies")
                yield Button("连接 (Connections)", id="conns")
                yield Button("日志 (Logs)", id="logs")
                yield Button("配置 (Config)", id="config")
        
            # 右侧面板现在是一个空的容器，将由代码动态填充
            with VerticalScroll(id="right-pane"):
                pass
                
        yield Footer()

    def on_mount(self) -> None:
        """当应用首次加载时调用，挂载默认页面。"""
        self.switch_page("overview")

    def switch_page(self, page_id: str) -> None:
        """切换右侧面板显示的页面。"""
        # 获取要挂载的页面类
        page_class = self.PAGES.get(page_id)
        if not page_class:
            return # 如果ID无效则不执行任何操作

        right_pane = self.query_one("#right-pane")
        # 移除所有旧的子组件（即旧页面）
        right_pane.remove_children()
        # 挂载新的页面组件实例
        right_pane.mount(page_class())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """当导航按钮被按下时，切换页面。"""
        # 移除所有按钮的 'active' CSS类
        for button in self.query("#left-pane Button"):
            button.remove_class("active")
        
        # 为当前被点击的按钮添加 'active' CSS类
        event.button.add_class("active")

        # 调用页面切换逻辑
        if event.button.id:
            self.switch_page(event.button.id)

def run():
    """运行应用。"""
    app = ClashUI()
    app.run()