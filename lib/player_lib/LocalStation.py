import os
import json
from datetime import datetime
from .helper import M3u8Parser, StationConfig, get_delta_time
from .station_interface import Station

os.path.dirname(os.path.abspath(__file__))

class LocalStation(Station):
    def __init__(self, my_station_settings_path):
        self.playlist_data = []

        self.playlist_start_index = 0
        self.start_ff_time = 0

        self.load_station_config_from_file(my_station_settings_path)
        self.set_station_config(self.station_config)

    def set_station_config(self, station_config) -> None:
        self.station_config = StationConfig(station_config)
        self.set_playlist_file()
        self.setup_playlist_data()
        self.set_timing()

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
                    "playlist_location": "",
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
            print(self.station_config.play_list_location)
            self.station_config.playlist_file =  self.station_config.play_list_location + 'default.m3u8'
        except:
            return

    def set_timing(self) -> None:
        ff = 0
        index = 0  

        if self.station_config.start_time > 0:
            ff = get_delta_time(self)

        for item in self.playlist_data:
            if ff > item.duration:
                ff -= item.duration
                index += 1
            else:
                break

        self.playlist_start_index = index
        self.start_ff_time = ff