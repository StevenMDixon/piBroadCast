import tkinter as tk
import os

class Window:
    def __init__(self, player):
        self.root = tk.Tk()
        self.root.title("VLC Media Player")
        self.player_frame = tk.Frame(self.root, bg="black")
        self.player_frame.pack(fill=tk.BOTH, expand=True)
        self.root.attributes('-fullscreen', True)
        self.currentPLayer = player

        self.setIDonPlayer()
        self.currentPLayer.play()
        self.run()

    def setWindowID(self):
            self.window_id = self.player_frame.winfo_id()
    
    def setIDonPlayer(self):
        self.setWindowID()
        # If windows
        if os.name == 'nt': 
            self.currentPLayer.getPlayer().set_hwnd(self.window_id)
        else:
            self.currentPLayer.getPlayer().set_xwindow(self.window_id)

    def run(self):
        self.root.mainloop()