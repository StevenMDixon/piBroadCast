import sys
from lib.player_lib.StationFactory import StationFactory
from lib.player_lib.Window import Window
from lib.player_lib.VLCPlayer import VLCPlayer

if __name__ == "__main__":
    command = ""

    if len(sys.argv) > 1:
        command = sys.argv[1]

    myStation = StationFactory.create_station(command)

    # Create a player
    vlcPlayer = VLCPlayer(myStation)

    window = Window()
    window.set_player(vlcPlayer)

    #run the window
    window.run()