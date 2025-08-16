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
                        video_files.append({'path': 'file:' + pathname2url(full_path), 'name': file, 'duration': duration, 'media_type': type, 'bumper_data': ''})

            return video_files
    
    @staticmethod
    def load_episodes_from_file(schedule_template_data):
            shows = {}
            locations_to_check = []

            videos = schedule_template_data['config']['schedule_items']
            for item in videos:
                name = item['name']
                locations = item['locations']

                drive_name = schedule_template_data['config']['drive_name']
                if "drive" in item:
                    drive_name = item["drive"] if item["drive"] != "" else drive_name

                for location in locations:
                     locations_to_check.append({'name': name, 'location': drive_name + location})

            for location in locations_to_check:
                directory_path = location['location'] 
                
                videos = VideoLoader._search_for_videos(directory_path, "show")

                if location['name'] in shows:
                    shows[location['name']] = shows[location['name']] + videos
                else:
                    shows[location['name']] = videos

            print(f"Found {len(shows)} shows")
            return shows
    
    @staticmethod
    def load_commercials(schedule_template_data, commercial_location):
        drive_name = schedule_template_data['drive_name']

        if "drive" in commercial_location:
            drive_name = commercial_location["drive"] if commercial_location["drive"] != "" else drive_name

        commercials = []

        for location in commercial_location["locations"]:
            commercials += VideoLoader._search_for_videos(drive_name + location, "commercial")

        print(f"Found {len(commercials)} commercials in {drive_name}")
        return commercials

    @staticmethod
    def load_bumpers(schedule_template_data, bumper_location):
         drive_name = schedule_template_data['drive_name']

         if "drive" in bumper_location:
             drive_name = bumper_location["drive"] if bumper_location["drive"] != "" else drive_name

         bumpers = []

         for location in bumper_location["locations"]:
             bumpers += VideoLoader._search_for_videos(drive_name + location, "bumper")

         print(f"Found {len(bumpers)} bumpers in {drive_name}")
         return bumpers