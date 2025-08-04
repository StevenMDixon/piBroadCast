import os
import json
from datetime import datetime
from .helper import M3u8Parser, StationConfig

os.path.dirname(os.path.abspath(__file__))

class LocalStation:
    def __init__(self, my_station_settings_path):
        self.playlist_data = []

        self.playlist_start_index = 0
        self.start_ff_time = 0

        station_config_data = self.load_station_config_from_file(my_station_settings_path)

        self.set_station_config(station_config_data)

    def set_station_config(self, station_config):
        self.station_config = StationConfig(station_config)
        self.set_playlist_file()
        self.setup_playlist_data()
        self.set_timing()

    def data_changed(self):
        return False

    def setup_playlist_data(self):
        if self.station_config.playlist_file:
            self.playlist_data = M3u8Parser.parsefile(self.station_config.playlist_file)

    def load_station_config_from_file(self, configPath):
        try: 
            with open(configPath, 'r') as file:
                # Load the JSON data from the file into a Python dictionary or list
                return json.load(file)
        except:
            return {
                    "station_name": "Error",
                    "subtitles": False,
                    "playlist_location": "",
                    "start_time": -1
            }

    def set_playlist_file(self):
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

    def set_timing(self):
        ff = 0
        index = 0  

        if self.station_config.start_time > 0:
            ff = self.get_delta_time()

        for item in self.playlist_data:
            if ff > item.duration:
                ff -= item.duration
                index += 1
            else:
                break

        self.playlist_start_index = index
        self.start_ff_time = ff
                

    def get_delta_time(self):
        current_time = datetime.now()
        daily_start_time = datetime.now().replace(hour= self.station_config.start_time, minute=0, second=0)
        # Need to calculate the delta between these
        return current_time.timestamp() - daily_start_time.timestamp()