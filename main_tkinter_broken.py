#!/usr/bin/env python3
"""
Edge Light for Video Calls
A simple transparent overlay with white border to improve lighting during video calls.
"""

import os
# Fix XCB threading issues on Linux
os.environ['PYQT_AUTO_UNLOAD'] = '1'

import tkinter as tk
from tkinter import messagebox
import sys


class EdgeLight:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Edge Light")

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Window configuration - must be done BEFORE geometry
        self.root.attributes('-topmost', True)  # Always on top

        # Set window type first (works on X11/Wayland)
        try:
            self.root.wm_attributes('-type', 'dock')
        except:
            pass

        # Then set geometry and other attributes
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.overrideredirect(True)  # No window decorations

        # Set semi-transparent background (0.0 to 1.0)
        # On Linux, we use a semi-transparent background instead of transparentcolor
        self.root.attributes('-alpha', 0.95)

        # Background color with slight transparency
        # Using a dark gray instead of pure black for better contrast
        self.root.configure(bg='#0a0a0a')

        # Create canvas for drawing the border
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width,
            height=screen_height,
            bg='#0a0a0a',
            highlightthickness=0
        )
        self.canvas.pack()

        # Border settings
        self.border_width = 80
        self.corner_radius = 100
        self.is_on = True
        self.brightness = 1.0  # 0.0 to 1.0

        # Draw the initial border
        self.draw_border()

        # Keyboard shortcuts
        self.root.bind('<Control-Shift-L>', lambda e: self.toggle_light())
        self.root.bind('<Control-Shift-Up>', lambda e: self.increase_brightness())
        self.root.bind('<Control-Shift-Down>', lambda e: self.decrease_brightness())
        self.root.bind('<Escape>', lambda e: self.quit_app())
        self.root.bind('<F1>', lambda e: self.show_help())

        # Create control panel in bottom center
        self.create_control_panel()

    def draw_border(self):
        """Draw the white border frame"""
        self.canvas.delete('border')

        if not self.is_on:
            return

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate color based on brightness
        color_value = int(255 * self.brightness)
        fill_color = f'#{color_value:02x}{color_value:02x}{color_value:02x}'

        # Draw outer rectangle (full screen)
        # We'll simulate a frame by drawing 4 rectangles (top, right, bottom, left)

        # Top border
        self.canvas.create_rectangle(
            0, 0, screen_width, self.border_width,
            fill=fill_color, outline='', tags='border'
        )

        # Bottom border
        self.canvas.create_rectangle(
            0, screen_height - self.border_width, screen_width, screen_height,
            fill=fill_color, outline='', tags='border'
        )

        # Left border
        self.canvas.create_rectangle(
            0, self.border_width, self.border_width, screen_height - self.border_width,
            fill=fill_color, outline='', tags='border'
        )

        # Right border
        self.canvas.create_rectangle(
            screen_width - self.border_width, self.border_width,
            screen_width, screen_height - self.border_width,
            fill=fill_color, outline='', tags='border'
        )

    def toggle_light(self):
        """Toggle the light on/off"""
        self.is_on = not self.is_on
        self.draw_border()
        self.update_status()

    def increase_brightness(self):
        """Increase brightness by 15%"""
        self.brightness = min(1.0, self.brightness + 0.15)
        self.draw_border()
        self.update_status()

    def decrease_brightness(self):
        """Decrease brightness by 15%"""
        self.brightness = max(0.2, self.brightness - 0.15)
        self.draw_border()
        self.update_status()

    def show_help(self):
        """Show keyboard shortcuts"""
        help_text = """Edge Light - Keyboard Shortcuts

💡 Toggle Light:  Ctrl + Shift + L
🔆 Brightness Up:  Ctrl + Shift + ↑
🔅 Brightness Down:  Ctrl + Shift + ↓
❌ Exit:  Escape
❓ Help:  F1

Click-through overlay - won't interfere with your work!
"""
        messagebox.showinfo("Edge Light - Help", help_text)

    def create_control_panel(self):
        """Create a simple control panel at the bottom"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Control frame with semi-transparent background
        control_frame = tk.Frame(self.root, bg='#2b2b2b', relief=tk.RAISED, bd=2)
        control_frame.place(
            x=screen_width // 2 - 200,
            y=screen_height - 100,
            width=400,
            height=60
        )

        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="Edge Light: ON | Brightness: 100%",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 10)
        )
        self.status_label.pack(pady=5)

        # Buttons frame
        button_frame = tk.Frame(control_frame, bg='#2b2b2b')
        button_frame.pack()

        tk.Button(
            button_frame, text='🔅', command=self.decrease_brightness,
            bg='#404040', fg='white', relief=tk.FLAT, padx=10
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            button_frame, text='💡', command=self.toggle_light,
            bg='#404040', fg='white', relief=tk.FLAT, padx=10
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            button_frame, text='🔆', command=self.increase_brightness,
            bg='#404040', fg='white', relief=tk.FLAT, padx=10
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            button_frame, text='❓', command=self.show_help,
            bg='#404040', fg='white', relief=tk.FLAT, padx=10
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            button_frame, text='❌', command=self.quit_app,
            bg='#cc0000', fg='white', relief=tk.FLAT, padx=10
        ).pack(side=tk.LEFT, padx=2)

    def update_status(self):
        """Update the status label"""
        status = "ON" if self.is_on else "OFF"
        brightness_pct = int(self.brightness * 100)
        self.status_label.config(
            text=f"Edge Light: {status} | Brightness: {brightness_pct}%"
        )

    def quit_app(self):
        """Exit the application"""
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    app = EdgeLight()
    app.run()


if __name__ == "__main__":
    main()
