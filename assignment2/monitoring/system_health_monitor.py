import psutil
import logging
from datetime import datetime

# Thresholds
CPU_THRESHOLD = 80  # percent
MEM_THRESHOLD = 80  # percent
DISK_THRESHOLD = 80  # percent
PROC_THRESHOLD = 300  # number of processes

# Setup logging
logging.basicConfig(
    filename='system_health.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def log_alert(message):
    print(message)
    logging.warning(message)

def check_system_health():
    alerts = []
    # CPU
    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_THRESHOLD:
        alerts.append(f"High CPU usage: {cpu}%")
    # Memory
    mem = psutil.virtual_memory().percent
    if mem > MEM_THRESHOLD:
        alerts.append(f"High Memory usage: {mem}%")
    # Disk
    disk = psutil.disk_usage('/').percent
    if disk > DISK_THRESHOLD:
        alerts.append(f"High Disk usage: {disk}%")
    # Processes
    proc_count = len(psutil.pids())
    if proc_count > PROC_THRESHOLD:
        alerts.append(f"High number of processes: {proc_count}")
    # Output summary
    print(f"CPU: {cpu}% | Memory: {mem}% | Disk: {disk}% | Processes: {proc_count}")
    if alerts:
        for alert in alerts:
            log_alert(alert)
    else:
        print("System health is normal.")

if __name__ == "__main__":
    check_system_health() 