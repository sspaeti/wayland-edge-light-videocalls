#!/usr/bin/env python3
"""
Calculate the exact window size that fits inside the edge light border.
Useful for manually positioning windows.
"""

import json
import subprocess

# Border width must match main.py
BORDER_WIDTH = 80

# Get monitor info from Hyprland
result = subprocess.run(['hyprctl', 'monitors', '-j'], capture_output=True, text=True)
monitors = json.loads(result.stdout)

if monitors:
    monitor = monitors[0]  # Primary monitor
    screen_width = monitor['width']
    screen_height = monitor['height']

    window_width = screen_width - (BORDER_WIDTH * 2)
    window_height = screen_height - (BORDER_WIDTH * 2)

    print(f"Screen: {screen_width}x{screen_height}")
    print(f"Border: {BORDER_WIDTH}px on each side")
    print(f"\nWindow size to fit inside border:")
    print(f"{window_width}x{window_height}")
    print(f"\nPosition (top-left corner): {BORDER_WIDTH},{BORDER_WIDTH}")
    print(f"\nHyprland windowrule:")
    print(f"windowrulev2 = size {window_width} {window_height}, title:^(YOUR_TITLE)")
    print(f"windowrulev2 = move {BORDER_WIDTH} {BORDER_WIDTH}, title:^(YOUR_TITLE)")
else:
    print("Could not get monitor information")
