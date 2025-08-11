import vlc

event_types = []

class VLCPlayer:
    def __init__(self, station):
        self.station = station
        # Options ['--file-caching=5000', '--network-caching=10000', '--verbose']
        self.instance = vlc.Instance()
        self.player = self.createListPlayer()
    
    def createListPlayer(self): 
        media_list = self.create_media_list(self.station)
       
        list_player = self.instance.media_list_player_new()
        media_player = self.instance.media_player_new()
        # media_player.video_set_aspect_ratio("4:3")
        # media_player.video_set_crop_geometry("680x480+0+0")
        # media_player.video_set_scale(2.5)

        list_player.set_media_player(media_player)
        list_player.set_media_list(media_list)

        return list_player
    
    def create_media_list(self, station):
        media_list = self.instance.media_list_new()

        if self.station.start_ff_time < 0:
            pre_schedule_media = self.instance.media_new('./signoff/color_bars.png', f':image-duration={station.start_ff_time * 1000}')
            media_list.add_media(pre_schedule_media)
            self.station.start_ff_time = 0

        for index, playlistitem in enumerate(station.playlist_data[station.playlist_start_index:]):
            media = self.instance.media_new(playlistitem.path)
            start_media_at = 0
                    
            if playlistitem.start_time_override > 0:
                start_media_at += playlistitem.start_time_override
            
            if index == 0:
                start_media_at += self.station.start_ff_time

            # setting start and stop times can be expensive, and may cause issues.
            if start_media_at > 0:
                media.add_option(f"start-time={start_media_at}")

            media.add_option(f"stop-time={playlistitem.end_time_override}")

            # Turn of hardware accelerated decoding as it causes some issues with videos on the rpi, 
            media.add_option(":avcodec-hw=none")

            media_list.add_media(media)

        #Appending an image to the end of the playlist in-case the time goes over
        media_list.add_media(self.instance.media_new('./signoff/color_bars.png'))
        
        return media_list
    
    def getPlayer(self):
        return self.player.get_media_player()
            
    def start(self):
        self.player.play()

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
            print("changing schedule")
            self.player.stop() 
            my_media_list = self.create_media_list(self.station)
            self.player.set_media_list(my_media_list)
            self.start()