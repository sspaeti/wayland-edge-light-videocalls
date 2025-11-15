# Edge Light for Video Calls

A lightweight Python/Tkinter application that adds a customizable glowing edge light effect around your screen. Perfect for ambient lighting during video calls on Linux.

Inspired by origin www.github.com:shanselman/WindowsEdgeLight and apple announcement sawn on Twitter.

## Features

- **Transparent Overlay**: Click-through design that doesn't interfere with your work
- **Customizable Brightness**: Adjust opacity from 20% to 100%
- **Toggle On/Off**: Quickly enable or disable the edge light effect
- **Always On Top**: Stays visible above all other windows
- **Keyboard Shortcuts**:
  - `Ctrl+Shift+L` - Toggle light on/off
  - `Ctrl+Shift+Up` - Increase brightness
  - `Ctrl+Shift+Down` - Decrease brightness
  - `Escape` - Exit application
  - `F1` - Show help
- **Control Panel**: Simple UI with buttons at the bottom of the screen

## Installation

### Prerequisites

- Python 3.8+ (comes with Tkinter)
- UV package manager

### Setup

The project is already initialized with UV. To run:

```bash
cd /home/sspaeti/Documents/sandbox/light-for-videocall
uv run main.py
```

## Usage

1. Run the application
2. A white border will appear around your screen edges
3. Use the control panel at the bottom or keyboard shortcuts to adjust
4. Press Escape to exit

## Hyprland Integration

### Launch Edge Light Only
Add to your Hyprland bindings:
```conf
bind = SUPER, E, exec, cd /home/sspaeti/Documents/sandbox/light-for-videocall && uv run main.py
```

### Window Rules for Browser Auto-Positioning
Add to your Hyprland config (e.g., `input.conf` or `hyprland.conf`):
```conf
# Auto-position Google Meet inside edge light border
windowrulev2 = float, title:^(Meet)
windowrulev2 = size 2720 1640, title:^(Meet)
windowrulev2 = move 80 80, title:^(Meet)
```

### Manual Window Positioning Shortcuts
Add keybindings to manually position any window:
```conf
bind = SUPER SHIFT, P, exec, hyprctl dispatch centerwindow
bind = SUPER SHIFT CTRL, P, resizeactive, exact 2720 1640
```

### Launch Script (Edge Light + Browser)
```bash
./launch-videocall.sh https://meet.google.com
```

The script uses your `$BROWSER` environment variable (defaults to Brave with Wayland flags).

## Technical Details

- Uses GTK4 with PyGObject for native Linux support
- Cairo drawing for smooth rendering
- Works with X11 and Wayland window managers (Hyprland compatible!)
- No XCB threading issues unlike Tkinter
- Designed for Hyprland/Arch Linux but should work on any Linux system

## Dependencies

On Arch Linux, you need these system packages:
```bash
sudo pacman -S gtk4 python-gobject python-cairo
```

The Python packages are managed by UV and installed automatically.

## Customization

Edit `main.py` to adjust:
- `border_width = 80` - Change border thickness (line 34)
- `brightness = 1.0` - Default brightness level (line 33)
- Window positioning and control panel location
