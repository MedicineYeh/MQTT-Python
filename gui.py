import tkinter as tk
import threading
import time

class TkinterGUI():
    def __init__(self, name):
        self.name = name
        # Config default values
        self.config = {
                    window_name: '580x240',
                    geometry: '580x240',
                }

    def callback(self):
        root.quit()

    def init(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        label = tk.Label(self.root, text="Hello World")
        label.pack()

        self.root.title(self.config.get("TITLE"))
        self.root.geometry(self.config.get("GEOMETRY"))
        # Config all custom GUI interfaces here

    def update(self):
        # do something
        self.root.update()

