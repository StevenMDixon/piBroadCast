import sys
from lib.player_lib.ServerStation import ServerStation
from lib.player_lib.LocalStation import LocalStation
from lib.player_lib.Window import Window
from lib.player_lib.VLCPlayer import VLCPlayer

if __name__ == "__main__":
    window = Window()

    if len(sys.argv) > 1:
        print(sys.argv)
        myStation = LocalStation(sys.argv[1])
    else:
        print("Running Server Player")
        myStation = ServerStation()

    # Create a player
    vlcPlayer = VLCPlayer(myStation)

    window.set_player(vlcPlayer)

    #run the window
    window.run()