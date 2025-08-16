import sys
from lib.player_lib.ServerStation import ServerStation
from lib.player_lib.LocalStation import LocalStation
from lib.player_lib.StreamStation import StreamStation
from lib.player_lib.Window import Window
from lib.player_lib.VLCPlayer import VLCPlayer

if __name__ == "__main__":
    window = Window()

    command = ""

    if len(sys.argv) > 1:
        command = sys.argv[1]

    if "http" in command:
        myStation = StreamStation(command)
    elif command != "":
        myStation = LocalStation(command)
    else:
        print("Running Server Player")
        myStation = ServerStation()

    # Create a player
    vlcPlayer = VLCPlayer(myStation)

    window.set_player(vlcPlayer)

    #run the window
    window.run()