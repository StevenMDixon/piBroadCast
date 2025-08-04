from dataclasses import dataclass

@dataclass
class EpisodeData:
    show_name: str
    episode_name: str
    episode_location: str
    episode_length: int
    media_type: str
    play_count: int = 0
    bumper_data: str = ""
    id: int = 0

    def __iter__(self):
        yield self.show_name
        yield self.episode_name
        yield self.episode_location
        yield self.episode_length
        yield self.media_type
        yield self.play_count
        yield self.bumper_data


@dataclass
class StationConfig:
    station_name: str
    subtitles: bool
    playlist_location: str
    playlist_file: str
    start_time: int
    id: int = 0    

    def __iter__(self):
        yield self.station_name
        yield self.subtitles
        yield self.playlist_location
        yield self.playlist_file
        yield self.start_time

@dataclass
class ScheduleTemplateData:
    template_data: bytes
    id: int = 0

    def __iter__(self):
        yield self.template_data

@dataclass
class ScheduleData:
    schedule_date: str
    schedule_file_name: str 
    id: int = 0

    def __iter__(self):
        yield self.schedule_date
        yield self.schedule_file_name
