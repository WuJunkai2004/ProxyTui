from textual.widgets import Static, Digits, Sparkline
from textual.containers import Widget, Grid, Vertical
from textual.reactive import reactive

from collections import deque
from json        import loads as JSONParser

from src import lang
from src import api
from src import config

class Form(Widget):
    DEFAULT_CSS = config.style("tss/over.css")
    upload   = reactive(0)
    download = reactive(0)
    memory   = reactive(0)
    conns    = reactive(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history_upload   = deque([0.0] * 60, maxlen=60)
        self.history_download = deque([0.0] * 60, maxlen=60)
        self.socket = api.API(config.URL, config.secret)
        self.stream = self.socket.getTraffic()
        self.memore = self.socket.getMemory()
        self.connes = self.socket.getConnections

    def compose(self):
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
            yield Sparkline(self.history_upload, id="upload-sparkline", summary_function=max)
            yield Sparkline(self.history_download, id="download-sparkline", summary_function=max)

    def on_mount(self):
        """挂载组件后，启动一个定时器每秒更新数据。"""
        self.update_timer = self.set_interval(1, self.update_stats)

    def update_stats(self) -> None:
        """
        更新所有统计数据的方法。由定时器调用。
        """
        up_down = JSONParser(next(self.stream))
        self.upload = round(up_down["up"] / 1024, 2)
        self.download = round(up_down["down"] / 1024, 2)
        self.memory = JSONParser(next(self.memore))['inuse']//(1024 * 1024)  # 转换为MB
        self.conns = len(JSONParser(self.connes()[1])['connections'])

        # 更新折线图的数据，确保值大于1以保证可见性
        self.history_upload  .append(self.upload)
        self.history_download.append(self.download)
        
        # 手动刷新Sparkline组件
        self.query_one("#upload-sparkline", Sparkline).data = list(self.history_upload)
        self.query_one("#download-sparkline", Sparkline).data = list(self.history_download)


    # 当响应式变量变化时，这些watch方法会自动被调用，从而更新UI
    def watch_upload(self, upload: int) -> None:
        self.query_one("#upload-digits", Digits).update(f"{upload}")

    def watch_download(self, download: int) -> None:
        self.query_one("#download-digits", Digits).update(f"{download}")

    def watch_memory(self, memory: int) -> None:
        self.query_one("#memory-digits", Digits).update(f"{memory}")

    def watch_conns(self, connections: int) -> None:
        self.query_one("#connections-digits", Digits).update(f"{connections}")