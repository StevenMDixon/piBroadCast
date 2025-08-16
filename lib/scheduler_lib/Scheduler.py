
import json
from datetime import date, datetime, timedelta
import calendar
from dataclasses import dataclass
import math
from lib.controller.Episode_Controller import Episode_Controller
from lib.controller.Schedule_Controller import Schedule_Controller
from lib.controller.Schedule_Template_Controller import Schedule_Template_Controller
from lib.controller.Station_Controller import Station_Controller
from lib.models.dto import ScheduleTemplateData, ScheduleData, StationConfig, EpisodeData
from lib.scheduler_lib.VideoLoader import VideoLoader
import random

@dataclass
class BlockItem:
        episode_data: EpisodeData
        start_time: int
        end_time: int

class Scheduler():
        def __init__(self, command = ""):
            self.stored_commercials = []
            self.stored_bumpers = []

            self.schedule_template_data = self.get_template_data()

            if self.schedule_template_data is None:
                  print("Run server.py and setup template before running")
                  quit()

            if command != "":
                print(f"running command: {command}")
                self.handle_command(command)

        def handle_command(self, command):
            match command:
                case '--Rebuild':
                        self.rebuild_data_base()
                        quit()
                case '--Build':
                        self.build_data_base()
                        quit()
                case '--Schedule':
                        self.create_schedule()

        @staticmethod
        def _decode(binary):
            decoded_string = binary.decode('utf-8')
            return json.loads(decoded_string)

        def get_template_data(self):
            schedule_template = Schedule_Template_Controller.get_current_schedule_template()
            data = ScheduleTemplateData(*schedule_template).template_data if schedule_template != None else None

            if data is None: return None
            return Scheduler._decode(data)

        def rebuild_data_base(self):
            Episode_Controller.delete_all_episode_metadata()
            Schedule_Controller.delete_all_schedules()
            self.build_data_base()

        def build_data_base(self):
            stored_shows = Episode_Controller.get_all_episode_metadata()
            if stored_shows:
                 print('Database is already seeded, run --Rebuild to rebuild the catalog')
                 quit()

            shows = VideoLoader.load_episodes_from_file(self.schedule_template_data)

            ready_to_insert = []
            for show in shows:
                 ready_to_insert += self.convert_to_episode_dto(show, shows[show])

            if self.schedule_template_data['config']['commercials']:
                commercial_locations = self.schedule_template_data['config']['commercials']
                for location_data in commercial_locations:
                    commercials = VideoLoader.load_commercials(self.schedule_template_data['config'], location_data)
                    ready_to_insert += self.convert_to_episode_dto('commercial', commercials)

                
            if self.schedule_template_data['config']['bumpers']:
                 for location_data in self.schedule_template_data['config']['bumpers']:
                    bumpers = VideoLoader.load_bumpers(self.schedule_template_data['config'], location_data)
                    ready_to_insert += self.convert_to_episode_dto('bumper', bumpers)

            Episode_Controller.insert_episodes(ready_to_insert)
            print(f"Shows and episodes added to db: {len(ready_to_insert)}. Run --Schedule to build playlists")

        def convert_to_episode_dto(self, show, episodes):
            converted = []
            for episode in episodes:
                converted.append(EpisodeData(show, episode['name'], episode['path'], episode['duration'], episode['media_type'], 0, episode['bumper_data']))

            return converted

        def create_schedule(self):
            self.start_scheduling_date = datetime.today().date()
            days_to_add = 0 
            self.most_recent_schedule = Schedule_Controller.get_lastest_schedule()

            if self.most_recent_schedule is not None:
                print(self.most_recent_schedule)
                self.start_scheduling_date = datetime.strptime(ScheduleData(*self.most_recent_schedule).schedule_date, "%Y-%m-%d").date()
                days_to_add = 1

            do_scheduling = True
            today = date(2025, 8, 28)
    
            if (today - self.start_scheduling_date).days < 0:
                do_scheduling = False

            if not do_scheduling:
                  print(f"scheduling has already been completed for this date {self.start_scheduling_date}")
                  quit()

            print(f"scheduling starting at: {self.start_scheduling_date}")

            # schedule_config = self.schedule_template_data['config']
            current_date = self.start_scheduling_date + timedelta(days_to_add)
            end_date = current_date + timedelta(days = 8)

            schedules = self.schedule_template_data['shedules']

            while current_date < end_date:
                self.create_days_schedule(schedules, current_date)
                current_date += timedelta(days=1)

        def create_days_schedule(self, schedules, date_to_schedule):
            stored_played_ids = []

            todays_name = calendar.day_name[date_to_schedule.weekday()]
            todays_schedule = schedules[todays_name] if todays_name  in schedules else schedules["default"] 

            schedule_stack = []

            for template_block in todays_schedule:
                block = self.schedule_block(template_block["duration"], template_block["show_name"], stored_played_ids)
                schedule_stack += block
                #update the played shows
                Episode_Controller.increment_played_count(list(map(lambda x: x.episode_data.id, block)))

            print(f"Schedule for {date_to_schedule} created with {len(schedule_stack)} items complete")
            # create the schedule object
            # Write the days shedule to file and update the db
            file_info = self.write_schedule_to_file(schedule_stack, date_to_schedule)
            Schedule_Controller.add_schedule(file_info)


        def schedule_block(self, duration, show_name, played) -> list[BlockItem]:
            episodes = Episode_Controller.get_all_episode_metadata_by_type_by_lowest_play_count('show', show_name, played)
            commercials = Episode_Controller.get_all_episode_metadata_by_type_by_lowest_play_count('commercial', 'commercial', [])
            bumpers = Episode_Controller.get_all_episode_metadata_by_type_by_lowest_play_count('bumper', 'bumper', [])

            fill_episode_duration = duration * 60
            block = []

            while fill_episode_duration > 0:
                test = list(filter(lambda x: x.id not in played, episodes))

                chosen_episode =  random.choice(test)

                episode_length_min = self._get_block_min_time(chosen_episode.episode_length)

                print(f"chosen episode {chosen_episode.episode_name} length {chosen_episode.episode_length} min {episode_length_min} fill time {fill_episode_duration}")

                block.append(BlockItem(chosen_episode, 0, chosen_episode.episode_length))

                block += self.fill_commercials_bumpers(episode_length_min - chosen_episode.episode_length, commercials, bumpers)

                played.append(chosen_episode.id)

                fill_episode_duration -= episode_length_min

            return block
            
        def fill_commercials_bumpers(self, remaining_time, commercials, bumpers) -> list[BlockItem]:
            bumper1 = random.choice(bumpers)
            bumper2 = random.choice(bumpers)

            remaining_time -= bumper1.episode_length
            remaining_time -= bumper2.episode_length

            selected_commercials = []

            while remaining_time > 0:
                selected_commercial = random.choice(commercials)

                remaining_time -= selected_commercial.episode_length

                offset = 0
                if remaining_time < 0:
                     offset = remaining_time

                selected_commercials.append(BlockItem(selected_commercial, 0, selected_commercial.episode_length + offset))

            return [BlockItem(bumper1, 0, bumper1.episode_length), *selected_commercials, BlockItem(bumper2, 0, bumper2.episode_length)]

        def write_schedule_to_file(self, schedule_data: list[BlockItem], date) :
            current_station_config = Station_Controller.get_current_station_config()
            directory = current_station_config.playlist_location

            template = "#EXTM3U\n"

            for block in schedule_data:
                template += f"#EXTINF:{block.episode_data.episode_length},{block.episode_data.episode_name},#x-start:{block.start_time}, #x-end:{block.end_time}\n"
                template += f"{block.episode_data.episode_location}\n"

            with open(f"{directory}{date}.m3u8", "w", encoding="utf-8") as file:
                 file.write(template)

            return {'schedule_date': date, 'schedule_file_name': directory + f"{date}.m3u8"}

        def _get_block_min_time(self, time):
            seconds = 60 * 15
            return seconds * math.ceil(time / seconds)


