import os
import json
from datetime import datetime
from .helper import M3u8Parser, StationConfig, PlayListItem
from lib.player_lib.StationInterface import IStation

os.path.dirname(os.path.abspath(__file__))

class StreamStation(IStation):
    def __init__(self, stream_url):
        
        self.playlist_start_index = 0
        self.start_ff_time = 0

        self.set_station_config({})

        self.playlist_data = [
            PlayListItem(stream_url, 9999999, start_time_override = 0, end_time_override = 9999999)
        ]

    def set_station_config(self, station_config) -> None:
        self.station_config = StationConfig(
            {
                "station_name": station_config.get("station_name", "Stream Station"),
                "playlist_location": "",
                "start_time": 0
            }
        )

    def data_changed(self) -> bool:
        return False

    def setup_playlist_data(self) -> None:
        return