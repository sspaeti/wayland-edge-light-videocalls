#!/bin/bash
# Position the active window inside the edge light border
# Automatically calculates size based on current monitor and scaling

BORDER_WIDTH=80  # Must match main.py (this is in logical/scaled pixels)

# Get the active monitor info
ACTIVE_MONITOR=$(hyprctl activeworkspace -j | jq -r '.monitor')
MONITOR_INFO=$(hyprctl monitors -j | jq ".[] | select(.name == \"$ACTIVE_MONITOR\")")

# Get physical resolution and scale
PHYSICAL_WIDTH=$(echo "$MONITOR_INFO" | jq -r '.width')
PHYSICAL_HEIGHT=$(echo "$MONITOR_INFO" | jq -r '.height')
SCALE=$(echo "$MONITOR_INFO" | jq -r '.scale')

# Convert scale to integer percentage (e.g., 2.0 -> 200, 1.8 -> 180)
# Remove decimal point and handle decimals
SCALE_INT=$(echo "$SCALE * 100" | awk '{printf "%.0f", $1}')

# GTK uses scaled coordinates, so the border is in scaled pixels
# Calculate effective/scaled resolution (use integer division)
SCREEN_WIDTH=$((PHYSICAL_WIDTH * 100 / SCALE_INT))
SCREEN_HEIGHT=$((PHYSICAL_HEIGHT * 100 / SCALE_INT))

# Calculate window size in scaled coordinates (subtract borders on both sides)
WIDTH_SCALED=$((SCREEN_WIDTH - BORDER_WIDTH * 2))
HEIGHT_SCALED=$((SCREEN_HEIGHT - BORDER_WIDTH * 2))

# But Hyprland uses physical pixels for window sizing
# So we need to scale back up
WIDTH=$((WIDTH_SCALED * SCALE_INT / 100))
HEIGHT=$((HEIGHT_SCALED * SCALE_INT / 100))

# Border position also needs to be in physical pixels
BORDER_OFFSET=$((BORDER_WIDTH * SCALE_INT / 100))

echo "Monitor: $ACTIVE_MONITOR"
echo "Screen: ${SCREEN_WIDTH}x${SCREEN_HEIGHT}"
echo "Window: ${WIDTH}x${HEIGHT}"

# Make window float if it isn't already
hyprctl dispatch togglefloating active

# Small delay to ensure window is floating
sleep 0.05

# Resize to exact size
hyprctl dispatch resizeactive exact ${WIDTH} ${HEIGHT}

# Move to exact position (border offset in physical pixels)
hyprctl dispatch moveactive exact ${BORDER_OFFSET} ${BORDER_OFFSET}
