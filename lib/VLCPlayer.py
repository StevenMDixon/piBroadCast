import vlc
import time

class VLCPlayer:
    def __init__(self, station):
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

        playlist = self.station.getPlaylist()

        media = self.instance.media_new(playlist)

        player.set_fullscreen(True)

        player.set_media(media)

        return player

    def createListPlayer(self): 
        player = self.instance.media_list_player_new()
        playlist = self.station.getPlaylist()

        media_list = self.instance.media_list_new()
        media_list.add_media(playlist)

        player.set_media_list(media_list)
        
        if self.station.subtitles:
            player.get_media_player().video_set_spu(0) 

        # current_media = media_player.get_media()
        # current_media.add_option("start-time=10726")
        return player

    def getPlayer(self):
        if not self.station.isStreamingStation:
            return self.player.get_media_player()
        else:
            return self.player
            
    def play(self):
        self.player.play()