import os
import json
from datetime import datetime
import time

class PlayListItem():
    def __init__(self, path, duration, start_time_override = 0, end_time_override = 0):
        self.path = path
        self.start_time_override = start_time_override if start_time_override > 0 else 0
        self.end_time_override = end_time_override if end_time_override > 0 else duration
        self.duration = (self.end_time_override if self.end_time_override < duration else duration) - self.start_time_override

class M3u8Parser():
    def parsefile(m3u8Src):
        myPlayList = list()
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

class Station:

    def __init__(self, stationConfigPath):
        stationConfig = self.loadStationConfig(stationConfigPath)
        self.stationName = stationConfig["station_name"]
        self.subtitles = bool(stationConfig["subtitles"])
        self.fileLocation = stationConfig["file_location"]
        self.playlistLocation = stationConfig["playlist_location"]
        self.startTime = stationConfig["start_time"]
        self.isStreamingStation = any(sub in self.playlistLocation for sub in ["http", "smb"])

        self.playlist_data = []
        self.playlist_src = ""

        self.playlist_start_index = 0
        self.start_ff_time = 0

        self.getPlaylist()
        self.setupPlaylistData()
        self.setTiming()

    def getPlaylist(self):
        #if the user provides a streaming service to load use that instead of local data
        if self.isStreamingStation: 
            return self.playlistLocation
        
        # Otherwise we are going to look for a playlist that matches that specific date
        try:
            contents = os.listdir(self.playlistLocation)
            today = datetime.today().strftime('%Y-%m-%d')
            for item in contents:
                if today in item:
                    self.playlist_src = self.playlistLocation + item
                    return

            self.playlist_src =  self.playlistLocation + 'default.m3u8'
        except:
            return
        
    def setupPlaylistData(self):
        self.playlist_data = M3u8Parser.parsefile(self.playlist_src)

    def loadStationConfig(self, configPath):
        try: 
            with open(configPath, 'r') as file:
                # Load the JSON data from the file into a Python dictionary or list
                data = json.load(file)

                return data
        except Exception as e:
            print(f"An error occurred: {e}")
            quit()

    def setTiming(self):
        ff = 0#self.getTimeToMoveTo
        index = 0  

        if self.startTime > 0:
            ff = self.getTimeToMoveTo()

        for item in self.playlist_data:
            if ff > item.duration:
                ff -= item.duration
                index += 1
            else:
                break

        self.playlist_start_index = index
        self.start_ff_time = ff
                

    def getTimeToMoveTo(self):
        currentTime = datetime.now()
        dailyStartTime = datetime.now().replace(hour= self.startTime, minute=0, second=0)

        # Need to calculate the delta between these
        return currentTime.timestamp() - dailyStartTime.timestamp()