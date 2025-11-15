#!/bin/bash
# Launch Edge Light + Browser for Video Calls
# Usage: ./launch-videocall.sh [URL]

EDGE_LIGHT_DIR="/home/sspaeti/Documents/sandbox/light-for-videocall"
BORDER_WIDTH=80  # Must match border_width in main.py

# Default to Google Meet if no URL provided
URL="${1:-https://meet.google.com}"

# Use the same browser config as Hyprland bindings.conf
# Default to brave if not set
BROWSER_CMD="${BROWSER:-uwsm app -- brave --new-window --ozone-platform=wayland --force-device-scale-factor=1.0}"

# Get screen resolution
SCREEN_WIDTH=$(hyprctl monitors -j | jq '.[0].width')
SCREEN_HEIGHT=$(hyprctl monitors -j | jq '.[0].height')

# Calculate window size (screen minus borders on both sides)
WINDOW_WIDTH=$((SCREEN_WIDTH - BORDER_WIDTH * 2))
WINDOW_HEIGHT=$((SCREEN_HEIGHT - BORDER_WIDTH * 2))

echo "Launching Edge Light..."
cd "$EDGE_LIGHT_DIR"
uv run main.py &
EDGE_LIGHT_PID=$!

# Wait for edge light to initialize
sleep 1

echo "Launching browser at $URL"
echo "Window size: ${WINDOW_WIDTH}x${WINDOW_HEIGHT}"

# Launch browser using the configured command
$BROWSER_CMD "$URL" &
BROWSER_PID=$!

# Wait a moment for window to appear
sleep 2

# Get the browser window address
WINDOW_ADDRESS=$(hyprctl clients -j | jq -r ".[] | select(.pid == $BROWSER_PID) | .address")

if [ -n "$WINDOW_ADDRESS" ]; then
    echo "Positioning browser window..."

    # Float the window
    hyprctl dispatch togglefloating address:$WINDOW_ADDRESS

    # Resize to fit inside border
    hyprctl dispatch resizewindowpixel exact ${WINDOW_WIDTH} ${WINDOW_HEIGHT},address:$WINDOW_ADDRESS

    # Center the window
    hyprctl dispatch centerwindow address:$WINDOW_ADDRESS

    echo "Setup complete!"
    echo "Edge Light PID: $EDGE_LIGHT_PID"
    echo "Browser PID: $BROWSER_PID"
else
    echo "Warning: Could not find browser window to position"
fi

# Keep script running to manage both processes
wait $EDGE_LIGHT_PID
