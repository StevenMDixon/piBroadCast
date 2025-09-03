import vlc
from urllib.request import pathname2url

instance = vlc.Instance()

# Create a Media Player object
player = instance.media_player_new()

file = pathname2url("I:\Commercials\Kids\[09.28.99] TnT Animal Farm Premiere.mp4")
print(file)
# Load your video file
media = instance.media_new("file:" + file) # Replace 'your_video_file.mp4' with your video path
player.set_media(media)

player.video_set_crop_geometry("4:3")

# Play the video
player.play()

while True:
    pass

