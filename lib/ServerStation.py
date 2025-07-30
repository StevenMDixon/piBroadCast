import os
import requests
from datetime import datetime
from .helper import M3u8Parser, StationConfig

class ServerStation:
    def __init__(self):
        self.playlist_data = []

        self.playlist_start_index = 0
        self.start_ff_time = 0

        station_config_data = self.load_station_config()
        self.set_station_config(station_config_data)
        

    def set_station_config(self, station_config):
        self.station_config = StationConfig(station_config)
        self.setup_playlist_data()
        self.set_timing()

    def data_changed(self):
        new_station_config_data = self.load_station_config()
        new_station = StationConfig(new_station_config_data)
        print(new_station)
        if new_station.playlist_src != self.station_config.playlist_src:
            self.set_station_config(new_station_config_data)
            return True
        else:
            return False

    def setup_playlist_data(self):
        if self.station_config.playlist_src:
            self.playlist_data = M3u8Parser.parsefile(self.station_config.playlist_src)

    def load_station_config(self):
        print("Pinging Home Base")
        url = "http://127.0.0.1:5000/station"
        response = requests.get(url)
        if response.status_code == 200:
            print("response:", response.json)
            return response.json()
        else:
            return ""

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