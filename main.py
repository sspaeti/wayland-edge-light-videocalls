#!/usr/bin/env python3
"""
Edge Light for Video Calls - GTK4 Version
A transparent overlay with white border to improve lighting during video calls.
Works properly on Linux with Wayland/X11.
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib
import sys


class EdgeLightWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window settings
        self.set_title("Edge Light")
        self.set_decorated(False)  # No window decorations

        # Get display and monitor info
        display = Gdk.Display.get_default()
        monitor = display.get_monitors()[0]  # Primary monitor
        geometry = monitor.get_geometry()

        # Set window to fullscreen on primary monitor
        self.set_default_size(geometry.width, geometry.height)
        self.fullscreen()

        # State
        self.is_on = True
        self.brightness = 1.0
        self.border_width = 80

        # Create main overlay container
        overlay = Gtk.Overlay()
        self.set_child(overlay)

        # Drawing area for the border
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_draw_func(self.draw_border)
        overlay.set_child(self.drawing_area)

        # Control panel
        self.create_control_panel(overlay)

        # Keyboard shortcuts
        self.setup_shortcuts()

    def draw_border(self, area, cr, width, height, user_data=None):
        """Draw the white border frame using Cairo"""
        if not self.is_on:
            # Clear everything
            cr.set_source_rgba(0, 0, 0, 0)
            cr.paint()
            return

        # Clear with transparent background
        cr.set_source_rgba(0, 0, 0, 0)
        cr.paint()

        # Set white color based on brightness
        cr.set_source_rgba(1.0, 1.0, 1.0, self.brightness)

        bw = self.border_width

        # Draw four rectangles for the border
        # Top
        cr.rectangle(0, 0, width, bw)
        cr.fill()

        # Bottom
        cr.rectangle(0, height - bw, width, bw)
        cr.fill()

        # Left
        cr.rectangle(0, bw, bw, height - 2 * bw)
        cr.fill()

        # Right
        cr.rectangle(width - bw, bw, bw, height - 2 * bw)
        cr.fill()

    def create_control_panel(self, overlay):
        """Create control panel at bottom center"""
        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        control_box.set_halign(Gtk.Align.CENTER)
        control_box.set_valign(Gtk.Align.END)
        control_box.set_margin_bottom(50)

        # Status label
        self.status_label = Gtk.Label(label=f"Edge Light: ON | Brightness: 100%")
        control_box.append(self.status_label)

        # Buttons
        btn_decrease = Gtk.Button(label="🔅 Dim")
        btn_decrease.connect("clicked", lambda b: self.decrease_brightness())
        control_box.append(btn_decrease)

        btn_toggle = Gtk.Button(label="💡 Toggle")
        btn_toggle.connect("clicked", lambda b: self.toggle_light())
        control_box.append(btn_toggle)

        btn_increase = Gtk.Button(label="🔆 Bright")
        btn_increase.connect("clicked", lambda b: self.increase_brightness())
        control_box.append(btn_increase)

        btn_quit = Gtk.Button(label="❌ Exit")
        btn_quit.connect("clicked", lambda b: self.close())
        control_box.append(btn_quit)

        overlay.add_overlay(control_box)

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_controller)

    def on_key_pressed(self, controller, keyval, keycode, state):
        """Handle keyboard shortcuts"""
        ctrl_shift = (state & Gdk.ModifierType.CONTROL_MASK) and (state & Gdk.ModifierType.SHIFT_MASK)

        if ctrl_shift and keyval == Gdk.KEY_l:
            self.toggle_light()
            return True
        elif ctrl_shift and keyval == Gdk.KEY_Up:
            self.increase_brightness()
            return True
        elif ctrl_shift and keyval == Gdk.KEY_Down:
            self.decrease_brightness()
            return True
        elif keyval == Gdk.KEY_Escape:
            self.close()
            return True

        return False

    def toggle_light(self):
        """Toggle the light on/off"""
        self.is_on = not self.is_on
        self.drawing_area.queue_draw()
        self.update_status()

    def increase_brightness(self):
        """Increase brightness by 15%"""
        self.brightness = min(1.0, self.brightness + 0.15)
        self.drawing_area.queue_draw()
        self.update_status()

    def decrease_brightness(self):
        """Decrease brightness by 15%"""
        self.brightness = max(0.2, self.brightness - 0.15)
        self.drawing_area.queue_draw()
        self.update_status()

    def update_status(self):
        """Update the status label"""
        status = "ON" if self.is_on else "OFF"
        brightness_pct = int(self.brightness * 100)
        self.status_label.set_text(f"Edge Light: {status} | Brightness: {brightness_pct}%")


class EdgeLightApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.edgelight.videocall")

    def do_activate(self):
        win = EdgeLightWindow(application=self)
        win.present()


def main():
    app = EdgeLightApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
