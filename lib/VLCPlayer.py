import vlc
import time

class VLCPlayer:
    def __init__(self, station):
        self.start_playing_index = 0
        self.start_playing_time = 0 
        self.station = station
        self.instance = vlc.Instance()
        self.setupPlayer()
        
    def setupPlayer(self):
        if not self.station.isStreamingStation:
            self.player = self.createListPlayer()
        else:
            self.player = self.createMediaPlayer()

    def createMediaPlayer(self):
        player = self.instance.media_player_new()

        playlist = self.station.playlist_src

        media = self.instance.media_new(playlist)

        player.set_fullscreen(True)

        player.set_media(media)

        return player

    def createListPlayer(self): 
            
        media_list = self.instance.media_list_new()
        
        # Add each media file from the playlist,
        # We don't need to enqueue files that will be skipped
        for index, playlistitem in enumerate(self.station.playlist_data, start=self.station.playlist_start_index):
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

        # Setup MediaListPlayer and attach MediaPlayer
        list_player = self.instance.media_list_player_new()
        media_player = self.instance.media_player_new()
        list_player.set_media_player(media_player)
        list_player.set_media_list(media_list)

        return list_player

    def getPlayer(self):
        if not self.station.isStreamingStation:
            return self.player.get_media_player()
        else:
            return self.player
            
    def start(self):
        if  self.station.isStreamingStation:
            self.player.play()
        else:
            self.player.play_item_at_index(self.station.playlist_start_index)

            
