#!/bin/bash
# Log errors for debugging
LOG_FILE="/tmp/edgelight-launch.log"
echo "=== Edge Light Launch $(date) ===" >> "$LOG_FILE"
cd ~/.local/bin/wayland-edge-light-videocalls 2>> "$LOG_FILE"
~/.local/bin/uv run main.py >> "$LOG_FILE" 2>&1
