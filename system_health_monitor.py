import psutil
import logging
from datetime import datetime

# Define thresholds
CPU_THRESHOLD = 80.0  # in percentage
MEMORY_THRESHOLD = 80.0  # in percentage
DISK_THRESHOLD = 80.0  # in percentage
PROCESS_THRESHOLD = 300  # number of processes

# Configure logging
logging.basicConfig(filename='system_health.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

def log_alert(message):
    logging.warning(message)

def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        log_alert(f"High CPU usage detected: {cpu_usage}%")

def check_memory_usage():
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    if memory_usage > MEMORY_THRESHOLD:
        log_alert(f"High Memory usage detected: {memory_usage}%")

def check_disk_space():
    disk_usage = psutil.disk_usage('/')
    disk_usage_percent = disk_usage.percent
    if disk_usage_percent > DISK_THRESHOLD:
        log_alert(f"Low Disk space detected: {disk_usage_percent}% used")

def check_running_processes():
    process_count = len(psutil.pids())
    if process_count > PROCESS_THRESHOLD:
        log_alert(f"High number of running processes detected: {process_count}")

def main():
    check_cpu_usage()
    check_memory_usage()
    check_disk_space()
    check_running_processes()

if __name__ == '__main__':
    main()
