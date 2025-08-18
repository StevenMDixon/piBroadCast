from lib.player_lib.ServerStation import ServerStation
from lib.player_lib.LocalStation import LocalStation
from lib.player_lib.StreamStation import StreamStation

class StationFactory:
    @staticmethod
    def create_station(source):
        if "http" in source:
            return StreamStation(source)
        elif source != "":
            return LocalStation(source)
        else:
            return ServerStation()
