#!/bin/bash
# Log errors for debugging
LOG_FILE="/tmp/edgelight-launch.log"
echo "=== Edge Light Launch $(date) ===" >> "$LOG_FILE"
cd /home/sspaeti/Documents/sandbox/light-for-videocall 2>> "$LOG_FILE"
/home/sspaeti/.local/bin/uv run main.py >> "$LOG_FILE" 2>&1
