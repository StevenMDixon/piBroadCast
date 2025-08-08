
class StationConfig():
    def __init__(self, station_config):
        self.station_name = station_config["station_name"]
        self.subtitles = bool(station_config["subtitles"])
        self.play_list_location = station_config["playlist_location"]
        self.start_time = station_config["start_time"]

        if "playlist_file" in station_config:
            self.playlist_file =  station_config["playlist_file"]
        else:
            self.playlist_file = ""

class PlayListItem():
    def __init__(self, path, duration, start_time_override = 0, end_time_override = 0):
        self.path = path
        self.start_time_override = start_time_override if start_time_override > 0 else 0
        self.end_time_override = end_time_override if end_time_override > 0 else duration
        self.og_duration = duration
        self.duration = (self.end_time_override if self.end_time_override < duration else duration) - self.start_time_override

class M3u8Parser():
    def parsefile(m3u8Src):
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
                    duration = int(metadata[0].split(':')[1])

                    for item in metadata:
                        if "#x-start:" in item:
                            start_time_override = int(item.split(":")[1])

                        if "#x-end:" in item:
                            end_time_override = int(item.split(":")[1])

                    path = file.readline().rstrip('\r\n')

                    myPlayList.append(PlayListItem(path, duration, start_time_override, end_time_override))
                    
            return myPlayList
        except Exception as ex:
            print("error occured:", ex)
            return myPlayList