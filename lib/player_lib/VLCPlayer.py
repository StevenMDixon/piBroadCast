from datetime import datetime
import vlc

event_types = []

class VLCPlayer:
    def __init__(self, station):
        self.station = station
        # Options ['--file-caching=5000', '--network-caching=10000', '--verbose=3']
        options = ['--no-skip-frames', '--no-xlib', '--file-caching=5000','--network-caching=5000', '--audio-filter=normvol', '--norm-max-level=1.00', '--gain=8.0']

        self.instance = vlc.Instance(options)

        if len(self.station.playlist_data) > 1:
            self.player = self.createListPlayer()
        else:
            self.player = self.createSinglePlayer()

    def createSinglePlayer(self) -> vlc.MediaPlayer:
        media = self.instance.media_new(self.station.playlist_data[0].path)
        # Turn off hardware accelerated decoding as it causes some issues with videos on the rpi,
        media.add_option(":avcodec-hw=none")

        player = self.instance.media_player_new()
        player.set_media(media)
        # player.video_set_aspect_ratio("4:3")
        player.video_set_crop_geometry("4:3")
        return player

    def createListPlayer(self) -> vlc.MediaListPlayer: 
        media_list = self.create_media_list(self.station)
       
        list_player = self.instance.media_list_player_new()
        media_player = self.instance.media_player_new()
        # media_player.video_set_aspect_ratio("4:3")
        media_player.video_set_crop_geometry("4:3")
        media_player.video_set_spu(-1)

        list_player.set_media_player(media_player)
        list_player.set_media_list(media_list)

        # list_player_event_manager = list_player.event_manager()
        media_player_event_manager = media_player.event_manager()

        media_player_event_manager.event_attach(vlc.EventType.MediaPlayerMediaChanged, self.media_changed_callback)

        # media_player_event_manager.event_attach(vlc.EventType.MediaPlayerPlaying, self.event_handler)
        # list_player_event_manager.event_attach(vlc.EventType.MediaListPlayerNextItemSet, self.event_handler)

        return list_player

    def create_media_list(self, station) -> vlc.MediaList:
        media_list = self.instance.media_list_new()

        if self.station.start_ff_time < 0:
            pre_schedule_media = self.instance.media_new('./signoff/standby.jpg', f':image-duration={station.start_ff_time * -1}')
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

            # Turn off hardware accelerated decoding as it causes some issues with videos on the rpi,
            media.add_option(":avcodec-hw=none")

            media_list.add_media(media)

        #Appending an image to the end of the playlist in-case the time goes over
        media_list.add_media(self.instance.media_new('./signoff/color_bars.png'))
        
        return media_list

    def getPlayer(self) -> vlc.MediaPlayer:
        if getattr(self.player, 'get_media_player', None) is None:
            return self.player
        
        return self.player.get_media_player()

    def start(self) -> None:
        self.player.play()

    def media_changed_callback(self, event):
        print(f"Media changed: {event.type}")
        player = self.player.get_media_player()
        current_show = player.get_media().get_mrl()

        current_show_metadata = filter(lambda x: x.path == current_show, self.station.playlist_data)

        if current_show_metadata is not None:
            show = list(current_show_metadata)[0]
            print(f"Current show: {show}")
            target_volume = self.calculate_vlc_volume(show.mean_volume)
            print(target_volume)
            player.audio_set_volume(target_volume)

    def periodic_task(self) -> None:
        if self.station.data_changed():
            print("changing schedule")
            self.player.stop() 
            my_media_list = self.create_media_list(self.station)
            self.player.set_media_list(my_media_list)
            self.start()
            
    def calculate_volume_gain_db(self, current_db, target_db=-18.0):
        return target_db - current_db  # positive = increase, negative = decrease
    
    def db_to_linear_gain(self, db):
        return 10 ** (db / 20)

    def calculate_vlc_volume(self, mean_db: float) -> int:
        gain_db = self.calculate_volume_gain_db(mean_db)
        gain_linear = self.db_to_linear_gain(gain_db)

        # Calculate the VLC volume based on the desired percentage of the mean.
        # Ensure the value is within VLC's valid range (0-100).
        target_vlc_volume =  int(min(max(gain_linear * 100, 0), 200))
        
        return target_vlc_volume