import tkinter as tk

class ToggleButton:
    def __init__(self, root, toggle=False, command=None):
        self.root = root
        self.command = command
        self.is_toggled = toggle
        self.toggle_button = tk.Button(root, text="Off", command=self.button_command)
        self.toggle_button.pack(pady=20)

    def button_command(self):
        if self.command:
            self.command()

        self.toggle()

    def toggle(self):
        self.is_toggled = not self.is_toggled

        if self.is_toggled:
            self.toggle_button.config(text="On")
        else:
            self.toggle_button.config(text="Off")