# plugins/system_info.py

import platform
import psutil
from datetime import datetime

def get_system_info() -> str:
    uname = platform.uname()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    cpu_freq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    info = f"""
🖥️ System Info
- OS: {uname.system} {uname.release}
- Version: {uname.version}
- Machine: {uname.machine}
- Processor: {uname.processor}
- Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}

🧠 CPU
- Physical cores: {psutil.cpu_count(logical=False)}
- Total cores: {psutil.cpu_count(logical=True)}
- Frequency: {cpu_freq.current:.2f} MHz
- Usage: {psutil.cpu_percent()}%

💾 Memory
- Total: {mem.total // (1024**3)} GB
- Used: {mem.used // (1024**3)} GB
- Free: {mem.available // (1024**3)} GB
- Usage: {mem.percent}%

📀 Disk
- Total: {disk.total // (1024**3)} GB
- Used: {disk.used // (1024**3)} GB
- Free: {disk.free // (1024**3)} GB
- Usage: {disk.percent}%

🌐 Network
- Sent: {net.bytes_sent // (1024**2)} MB
- Received: {net.bytes_recv // (1024**2)} MB
"""
    return info.strip()
