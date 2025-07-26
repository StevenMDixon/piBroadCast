import os
import json
from datetime import datetime
import time

class Station:

    def __init__(self, stationConfigPath):
        stationConfig = self.loadStationConfig(stationConfigPath)
        self.stationName = stationConfig["station_name"]
        self.subtitles = bool(stationConfig["subtitles"])
        self.fileLocation = stationConfig["file_location"]
        self.playlistLocation = stationConfig["playlist_location"]
        self.startTime = stationConfig["start_time"]
        self.isStreamingStation = any(sub in self.playlistLocation for sub in ["http", "smb"])
        
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
                    return self.playlistLocation + item
                
            return self.playlistLocation + 'default.m3u8'
        except:
            return ""

    def loadStationConfig(self, configPath):
        try: 
            with open(configPath, 'r') as file:
                # Load the JSON data from the file into a Python dictionary or list
                data = json.load(file)
                return data
        except Exception as e:
            print(f"An error occurred: {e}")
            quit()

    def getTimeToMoveTo(self):
        currentTime = datetime.now()

        dailyStartTime = datetime.now().replace(hour= self.startTime, minute=0, second=0)

        # Need to calculate the delta between these
        return currentTime.timestamp() - dailyStartTime.timestamp()