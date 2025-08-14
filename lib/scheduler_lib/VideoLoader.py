from urllib.request import pathname2url
import ffmpeg
import os

video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v')

class VideoLoader:
    @staticmethod
    def _search_for_videos(target_directory, type):
            video_files = []

            for root, _, files in os.walk(target_directory):
                for file in files:
                    if file.lower().endswith(video_extensions):
                        full_path = os.path.join(root, file)
                        
                        duration = float(ffmpeg.probe(full_path)["format"]["duration"])
                        #m3u8 files dont have floating points, so we'll just round down :-)
                        video_files.append({'path': 'file:' + pathname2url(full_path), 'name': file, 'duration': int(duration), 'media_type': type, 'bumper_data': ''})

            return video_files
    
    @staticmethod
    def load_episodes_from_file(schedule_template_data):
            shows = {}
            locations_to_check = []

            videos = schedule_template_data['config']['schedule_items']
            for item in videos:
                name = item['name']
                locations = item['locations']

                for location in locations:
                     locations_to_check.append({'name': name, 'location': location})

            drive_name = schedule_template_data['config']['drive_name']

            for location in locations_to_check:
                directory_path = location['location'] 
                
                videos = VideoLoader._search_for_videos(drive_name + directory_path, "show")

                if location['name'] in shows:
                    shows[location['name']] = shows[location['name']] + videos
                else:
                    shows[location['name']] = videos

            return shows
    
    @staticmethod
    def load_commercials(schedule_template_data):
        commercial_location  = schedule_template_data['commercials']
        drive_name = schedule_template_data['drive_name']

        commercials = VideoLoader._search_for_videos(drive_name + commercial_location, "commercial")

        return commercials

    @staticmethod
    def load_bumpers(schedule_template_data):
         bumper_location = schedule_template_data['bumpers']
         drive_name = schedule_template_data['drive_name']

         bumpers = VideoLoader._search_for_videos(drive_name + bumper_location, "bumper")
         
         return bumpers