import os
from lib.Station import Station
from lib.Window import Window
from lib.VLCPlayer import VLCPlayer

os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # Look for settings file, this should be local?
    # I imagine we should be able to overwrite this
    setting_file_path = 'template/settings.json'

    myStation = Station(setting_file_path)

    # Create a player
    vlcPlayer = VLCPlayer(myStation)

    # Setup a window
    window = Window(vlcPlayer)

    #run the window
    window.run()