import tkinter as tk
import os

class Window:
    def __init__(self, ):
        self.root = tk.Tk()
        self.root.title("VLC Media Player")
        self.player_frame = tk.Frame(self.root, bg="black")
        self.player_frame.pack(fill=tk.BOTH, expand=True)
        self.root.attributes('-fullscreen', True)

        self.current_player = None
        self.root.bind("<KeyPress>", self.handleKeyPress)

    def set_player(self, vlc_player):
        self.current_player = vlc_player
        self.setIDonPlayer()
        self.current_player.start()
        self.run()

    def setWindowID(self):
            self.window_id = self.player_frame.winfo_id()
    
    def setIDonPlayer(self):
        self.setWindowID()
        # If windows
        if os.name == 'nt': 
            self.current_player.getPlayer().set_hwnd(self.window_id)
        else:
            self.current_player.getPlayer().set_xwindow(self.window_id)
    
    def handleKeyPress(self, event):
         if self.current_player is not None:
            self.current_player.handleKeyPress(event.keycode)

    def run_player_tasks(self):
         print("Running Periodic Tasks")
         self.current_player.periodic_task()
         self.root.after(5000, self.run_player_tasks)
    
    def run(self):
        if self.current_player is not None:
             self.root.after(5000, self.run_player_tasks)
             
        self.root.mainloop()