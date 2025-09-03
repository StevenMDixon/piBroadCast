import os
import json
from datetime import datetime
from .helper import M3u8Parser, StationConfig, get_timing_data
from lib.player_lib.StationInterface import  IStation

os.path.dirname(os.path.abspath(__file__))

class LocalStation(IStation):
    def __init__(self, my_station_settings_path):
        self.playlist_data = []

        self.playlist_start_index = 0
        self.start_ff_time = 0

        self.load_station_config_from_file(my_station_settings_path)
        self.set_station_config(self.station_config)
        print(self.playlist_data)

    def set_station_config(self, station_config) -> None:
        self.station_config = StationConfig(station_config)
        self.set_playlist_file()
        print(self.station_config.playlist_file)
        self.setup_playlist_data()
        timing_data = get_timing_data(self.station_config.start_time, self.playlist_data)
        self.playlist_start_index = timing_data["index"]
        self.start_ff_time = timing_data["start"]

    def data_changed(self) -> bool:
        return False

    def setup_playlist_data(self) -> None:
        if self.station_config.playlist_file:
            self.playlist_data = M3u8Parser.parsefile(self.station_config.playlist_file)

    def load_station_config_from_file(self, configPath) -> None:
        try: 
            with open(configPath, 'r') as file:
                # Load the JSON data from the file into a Python dictionary or list
                self.station_config = json.load(file)
        except:
            self.station_config = {
                    "station_name": "Error",
                    "playlist_location": "./playlists/",
                    "start_time": -1
            }

    def set_playlist_file(self) -> None:
        try:
            contents = os.listdir(self.station_config.play_list_location)
            today = datetime.today().strftime('%Y-%m-%d')
            for item in contents:
                print(today, item)
                if today in item:
                    self.station_config.playlist_file = self.station_config.play_list_location + item
                    return
            
            self.station_config.playlist_file =  self.station_config.play_list_location + 'default.m3u8'
        except:
            return