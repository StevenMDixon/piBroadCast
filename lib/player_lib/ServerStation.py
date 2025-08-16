from datetime import datetime
from .helper import M3u8Parser, get_delta_time
from lib.controller.Station_Controller import Station_Controller
from lib.controller.Schedule_Controller import Schedule_Controller

class ServerStation:
    def __init__(self):
        self.playlist_data = []

        self.playlist_start_index = 0
        self.start_ff_time = 0

        self.playlist = ""

        station_config_data = self.load_station_config()
        self.set_station_config(station_config_data)
        print(self.playlist_start_index, self.start_ff_time)
        
    def set_station_config(self, station_config):
        self.station_config = station_config
        self.data_changed()

    def data_changed(self):
        todays_schedule = Schedule_Controller.get_todays_schedule(datetime.today().date())
        
        if todays_schedule is None:
            return False
        
        if self.playlist != todays_schedule.schedule_file_name:
            self.playlist = todays_schedule.schedule_file_name

            self.setup_playlist_data()
            self.set_timing()
            return True
        else:
            return False

    def setup_playlist_data(self):
        if self.playlist:
            self.playlist_data = M3u8Parser.parsefile(self.playlist)

    def load_station_config(self):
        return Station_Controller.get_current_station_config()

    def set_timing(self):
        ff = 0
        index = 0  

        if self.station_config.start_time > 0:
            ff = get_delta_time(self)
            print(ff)

        for item in self.playlist_data:
            if ff > item.duration:
                ff -= item.duration
                index += 1
            else:
                break

        self.playlist_start_index = index
        self.start_ff_time = ff
                

    