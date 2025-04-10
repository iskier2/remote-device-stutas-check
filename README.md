# Remote Device Status Check

## Overview

This project is designed to monitor the operational status of network devices using SSH tunneling and CSV parsing. The monitoring workflow involves:

- Establishing an SSH tunnel from a local machine through an intermediary server (Server A) to a target server (Server B).
- Downloading the `network_devices.csv` file from `/home/stauto/` on Server B.
- Parsing the CSV file to create a dynamic list of objects with properties based on the CSV header.
- Enforcing strict type validation
- Logging any invalid CSV entries to a log file named `test_log.log`.
- Monitoring initially "online" devices periodically (every 20 seconds) during a custom timeout period specified by the `--timeout` command-line option. If any device goes offline during this period, the test fails immediately.

## Requirements

- Python 3.8+
- Environment variables:
  - `SERVER_A_ADDRESS`
  - `SERVER_B_ADDRESS`
  - `SERVER_A_KEY`
  - `SERVER_B_KEY`

## Installation

Install dependencies using:

```bash
pip install -r requirements.txt
