from urllib.request import pathname2url
import ffmpeg
import os
import sys

video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v')

if __name__ == "__main__":
    directory = None

    if len(sys.argv) > 1:
        directory = sys.argv[1]

    if directory is None or not os.path.exists(directory):
        print("Please provide a valid directory")
        sys.exit(1)

    video_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(video_extensions):
                full_path = os.path.join(root, file)
                
                duration = float(ffmpeg.probe(full_path)["format"]["duration"])

                mean_volume = 0
                max_volume = 0
                try:
                    
                    probe = ffmpeg.input(full_path).audio.filter("volumedetect").output("null", f="null").run(capture_stderr=True)

                    # Extract volume information from the stderr output
                    stderr_output = probe[1].decode("utf-8")
                    
                    # Parse the output to find mean_volume and max_volume
                    mean_volume_line = next(line for line in stderr_output.splitlines() if "mean_volume" in line)
                    max_volume_line = next(line for line in stderr_output.splitlines() if "max_volume" in line)
                    
                    mean_volume = float(mean_volume_line.split(":")[1].strip().replace(" dB", ""))
                    max_volume = float(max_volume_line.split(":")[1].strip().replace(" dB", ""))

                except ffmpeg.Error as e:
                    print(f"FFmpeg Error: {e.stderr.decode('utf-8')}")
                except Exception as e:
                    print(f"An error occurred: {e}")
                
                video_files.append({'path': 'file:' + pathname2url(full_path), 'name': file, 'duration': duration, 'media_type': type, 'tags': '', 'mean_volume': mean_volume, 'max_volume': max_volume})

                if mean_volume < -30:
                    print(f"Low mean volume detected in {file}: {mean_volume} dB")

    print(video_files)