
from .helper import M3u8Parser, get_timing_data
from datetime import datetime
from lib.controller.Station_Controller import Station_Controller
from lib.controller.Schedule_Controller import Schedule_Controller
from lib.player_lib.StationInterface import IStation

class ServerStation(IStation):
    def __init__(self):
        self.playlist_data = []

        self.playlist_start_index = 0
        self.start_ff_time = 0

        self.playlist = ""

        self.load_station_config()
        self.set_station_config(self.station_config)

    def set_station_config(self, station_config) -> None:
        self.station_config = station_config
        self.data_changed()

    def data_changed(self) -> bool:
        todays_schedule = Schedule_Controller.get_todays_schedule(datetime.today().date())
        
        if todays_schedule is None:
            return False
        
        if self.playlist != todays_schedule.schedule_file_name:
            self.playlist = todays_schedule.schedule_file_name

            self.setup_playlist_data()
            timing_data = get_timing_data(self.station_config.start_time, self.playlist_data)
            self.playlist_start_index = timing_data["index"]
            self.start_ff_time = timing_data["start"]
            return True
        else:
            return False

    def setup_playlist_data(self) -> None:
        if self.playlist:
            self.playlist_data = M3u8Parser.parsefile(self.playlist)

    def load_station_config(self) -> None:
        self.station_config = Station_Controller.get_current_station_config()

    