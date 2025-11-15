# Edge Light for Video Calls

A lightweight Python/Tkinter application that adds a customizable glowing edge light effect around your screen. Perfect for ambient lighting during video calls on Linux!

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

You can add a keybinding to your Hyprland config to launch it:

```conf
# ~/.config/hypr/hyprland.conf or your tiling.conf
bind = SUPER, E, exec, cd /home/sspaeti/Documents/sandbox/light-for-videocall && uv run main.py
```

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
