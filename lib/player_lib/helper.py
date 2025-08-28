from datetime import datetime, timedelta

def get_delta_time(start_time) -> float:
        current_time = datetime.now()
        daily_start_time = datetime.now().replace(hour= start_time, minute=0, second=0)
        # Need to calculate the delta between these
        return current_time.timestamp() - daily_start_time.timestamp()

def get_timing_data(start_time, playlist) -> dict:
    ff = 0
    index = 0  

    if(start_time > 0):
        ff = get_delta_time(start_time)

    for item in playlist:
        if ff > item.duration:
            ff -= item.duration
            index += 1
        else:
            break

    return {"start": ff, "index": index}

class StationConfig():
    def __init__(self, station_config):
        self.station_name = station_config["station_name"]
        self.play_list_location = station_config["playlist_location"]
        self.start_time = station_config["start_time"]

        if "playlist_file" in station_config:
            self.playlist_file =  station_config["playlist_file"]
        else:
            self.playlist_file = ""

class PlayListItem():
    def __init__(self, path, duration, start_time_override = 0, end_time_override = 0, mean_volume = 0):
        self.path = path
        self.start_time_override = start_time_override if start_time_override > 0 else 0
        self.end_time_override = end_time_override if end_time_override > 0 else duration
        self.og_duration = duration
        self.duration = (self.end_time_override if self.end_time_override < duration else duration) - self.start_time_override
        self.mean_volume = mean_volume

class M3u8Parser():
    def parsefile(m3u8Src) -> list[PlayListItem]:
        print(m3u8Src)
        myPlayList = list()
        try:
            with open(m3u8Src, "r") as file:
                header = file.readline()
                while True:
                    metadata = file.readline().split(',')

                    if not metadata or metadata[0] == '':
                        break
                    start_time_override = 0
                    end_time_override = 0
                    duration = float(metadata[0].split(':')[1])

                    for item in metadata:
                        if "#x-start:" in item:
                            start_time_override = float(item.split(":")[1])

                        if "#x-end:" in item:
                            end_time_override = float(item.split(":")[1])
                        
                        if "#x-mean-vol:" in item:
                            mean_volume = float(item.split(":")[1])

                    path = file.readline().rstrip('\r\n')

                    myPlayList.append(PlayListItem(path, duration, start_time_override, end_time_override, mean_volume))

            return myPlayList
        except Exception as ex:
            print("error occured:", ex)
            return myPlayList