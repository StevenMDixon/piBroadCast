import vlc
import time
import requests
import json

event_types = []

class VLCPlayer:
    def __init__(self, station):
        self.start_playing_index = 0
        self.start_playing_time = 0 
        self.station = station
        # ['--file-caching=5000', '--network-caching=10000', '--verbose']
        self.instance = vlc.Instance()
        self.player = self.createListPlayer()
        
    
    def createListPlayer(self): 
        media_list = self.create_media_list(self.station)
       
        list_player = self.instance.media_list_player_new()
        media_player = self.instance.media_player_new()
        list_player.set_media_player(media_player)
        list_player.set_media_list(media_list)
        return list_player
    
    def create_media_list(self, station):
        media_list = self.instance.media_list_new()
        
        if not station.playlist_data:
            #if we don't have any data we are offline
            media_list.add_media(self.instance.media_new('./signoff/color_bars.png'))
            return media_list

        for index, playlistitem in enumerate(station.playlist_data, start=station.playlist_start_index):
            media = self.instance.media_new(playlistitem.path)
            start_media_at = 0
                    
            if playlistitem.start_time_override > 0:
                start_media_at += playlistitem.start_time_override
            
            if index == self.station.playlist_start_index:
                start_media_at += self.station.start_ff_time

            media.add_option(f"start-time={start_media_at}")

            if playlistitem.end_time_override > 0:
                media.add_option(f"stop-time={playlistitem.end_time_override}")

            media_list.add_media(media)
        return media_list
    
    def getPlayer(self):
        return self.player.get_media_player()
            
    def start(self):
        self.player.play_item_at_index(self.station.playlist_start_index)

    # def handleEvent(self, event):
    #     print(f" Event fired: {event.type} | {vlc.EventType(event.type).name}")

    #implemented in window to pass key presses to the player
    def handleKeyPress(self, keypress):
        # # if we press the space bar resume playing
        # if keypress == 32:
        #     my_media_list = self.create_media_list(self.station)
        #     self.player.stop()
        #     self.player.set_media_list(my_media_list)
        #     self.player.play()
        # print(keypress)
        return

    def periodic_task(self):
        if self.station.data_changed():
            print("changing station")
            self.player.stop() 
            my_media_list = self.create_media_list(self.station)
            self.player.set_media_list(my_media_list)
            self.player.play()