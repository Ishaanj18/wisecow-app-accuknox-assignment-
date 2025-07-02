import requests
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='app_health.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def check_app_health(url):
    try:
        response = requests.get(url, timeout=5)
        status = response.status_code
        if 200 <= status < 400:
            msg = f"{url} is UP (HTTP {status})"
            print(msg)
            logging.info(msg)
        else:
            msg = f"{url} is DOWN (HTTP {status})"
            print(msg)
            logging.warning(msg)
    except Exception as e:
        msg = f"{url} is DOWN (Exception: {e})"
        print(msg)
        logging.error(msg)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app_health_checker.py <URL>")
        sys.exit(1)
    check_app_health(sys.argv[1]) 