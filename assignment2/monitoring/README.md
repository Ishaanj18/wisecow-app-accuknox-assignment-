# Assignment 2: Monitoring Scripts

This folder contains two Python scripts for system and application health monitoring:

## 1. System Health Monitoring Script
- **File:** `system_health_monitor.py`
- **Description:** Checks CPU, memory, disk usage, and process count. Alerts if any metric exceeds thresholds.
- **Usage:**
  ```sh
  python system_health_monitor.py
  ```
- **Logs:** Alerts are printed to the console and written to `system_health.log`.

## 2. Application Health Checker
- **File:** `app_health_checker.py`
- **Description:** Checks the HTTP status of a given URL and reports if the application is up or down.
- **Usage:**
  ```sh
  python app_health_checker.py <URL>
  # Example:
  python app_health_checker.py https://www.google.com
  ```
- **Logs:** Results are printed to the console and written to `app_health.log`.

## Requirements
- Python 3.x
- `psutil` and `requests` libraries:
  ```sh
  pip install psutil requests
  ```
