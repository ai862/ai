# file: forward_to_xray.py
from mitmproxy import http, proxy
import logging

# --- 配置区 ---

# 1. 设置你想要扫描的目标 host 列表
#    我已经将您日志中的 IP 地址添加进去了
TARGET_HOSTS = [
    "10.211.55.39", 
    # 在这里可以继续添加其他域名，例如:
    # "your-target-site.com",
]

# 2. 设置 Xray 的监听地址和端口
XRAY_ADDRESS = "127.0.0.1"
XRAY_PORT = 7001

# --- 配置区结束 ---

# 配置一个简单的日志记录器
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [Redirector] - %(message)s'
)

class XrayRedirector:
    """
    一个 mitmproxy 插件，用于在 TCP 连接层面将特定流量重定向到 Xray。
    """
    def server_connect(self, data: proxy.server_hooks.ServerConnectionHookData):
        """
        mitmproxy 的服务器连接事件处理函数。
        这个钩子在 mitmproxy 准备连接到上游服务器之前触发，是重定向流量的最佳时机。
        """
        # data.server.address 是 mitmproxy 打算连接的目标地址
        intended_host = data.server.address[0]

        if intended_host in TARGET_HOSTS:
            # 这是最关键的修正！
            # 我们不再在 HTTP 请求层面操作，而是在 TCP 连接层面直接重定向。
            # 当 mitmproxy 打算连接到我们列表中的目标时，我们修改这个连接的目的地，
            # 让它实际连接到 Xray。
            # 这样，mitmproxy 就成了 Xray 的客户端，将所有数据原样转发给 Xray。
            
            logging.info(f"匹配到目标 Host: {intended_host} -> 重定向 TCP 连接到 Xray@{XRAY_ADDRESS}:{XRAY_PORT}")
            
            data.server.address = (XRAY_ADDRESS, XRAY_PORT)

# mitmproxy 加载插件需要一个 addons 列表
addons = [
    XrayRedirector()
]
