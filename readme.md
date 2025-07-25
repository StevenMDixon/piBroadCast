# piBroadCast

piBroadCast is a attempt at making a simple but effect home broadcast solution. This solution should be scalable and each pi will act as an individual station, programmed with old commercials and bumpers!

I would like to give credit for my inspiration around this project to Shane Mason, his work on FieldStation42 is amazing and you should check it out if you want a more feature rich solution.
https://github.com/shane-mason/FieldStation42/tree/main

## Why, tho?

I wanted to be able to play old media across my home via coaxial cables. Obviously going through my mid-life crisis here :-)

I also wanted to have a strict control over what is being seen by my child, without potentially giving them access to the internet.


## The Ideal setup (mine)

The plan is to use 4 Raspberry pi's being piped into a `Channel Plus Box Model 5545 Quad Digital Modulator` that will result in any tv in the house being able to pickup 4 channels that are specified from the QuadRF

```
Pi 1 ______
Pi 1 ______|               
Pi 3 ______|                    
Pi 4 ______|____QuadRF___Home Coaxial Setup ______ 4 Channels on reciever 
```

So long as you have a way to mix signals before piping it into your walls you theoretically could expand this past the 4 channels, at that point it may be more cost effective to go with a software solution instead.

4 channels is all I really need, I'm located in GA, and I plan on use channels 13, 32, 33, 34 for this project. IFYKYK

Media takes up a ton of space, so how do we get it to the pi?

We can actually use a couple methods!
1. External HDD/USB
2. Network shares, VLC can mount smb shares and network drives!
3. Copy files directly to the pi's internal system

## Setting up a raspberry pi

We need to setup the the rpi 4 to output composite signal for our rf modulator.

Always upgrade your firmware before doing this, there used to be a slowdown issue that was resolved for the rpi 4 models.
You may have to connect to hdmi to do this part, check out the rpi docs to update your firmware.

In config.txt

Change 
```
# Enable DRM VC4 V3D driver
dtoverlay=vc4-kms-v3d
```
To
```
# Enable DRM VC4 V3D driver
dtoverlay=vc4-kms-v3d,composite
```

Then add this anywhere
```
enable_tvout=1
sdtv_mode=0
sdtv_aspect=4:3
```

sdtv_mode = 0 is for NTSC, there a ton of other modes to choose from check the official docs for those values

In cmdline.txt add this to the end

```
video=Composite-1:640x480@60ie,margin_left=40,margin_right=40,margin_top=32,margin_bottom=32
```

You may need to edit your margins. YMMV.

Also depending on your composite cables red and yellow may be swapped.


## Development

First and foremost I need to figure out the best way to play video in the standard pi environment.

I've chosen to use docker for this project, because I will need to run the rpi image there for testing.

I want the ability to swap content on the PI pretty easily and have chosen to put the content on an external usb.

Station Content Layout:
```
/External_Drive
    Schedule.json
    Settings.json
    /Shows
        /Show 1
        /Show 2
    /Commercials
    /Bumps
```

I am thinking I use Python to create a playlist for vlc and load that up.
We can check what the current time is and move to the correct location in the playlist?

Turns out we can!
 vlc --playlist /path/to/your/playlist.m3u --start-time=seconds

 So we can to generate a playlist?

Maybe a better version of this may be to use mpv a la; from python_mpv_jsonipc import MPV?
 I am seeing a ton of conflicting info around mpv so I am gonna stick with vlc for this project.


## Scheduling

We need to generate a dynamic schedule for a (day || week)

using kwb as an example, their schedule was something like
8-11a.m. (3 hours or 6 episodes)
-- We can figure out how to stick a we'll be back message here, or just fill it with random non-sequential episodes or reruns of the previous block
11-3p.m. (4 hours or 8 episodes [Reruns][Non-Sequential])
3-5p.m. (2 hours or 4 episodes)
5-8p.m. (3 hours 6 episodes [Reruns][Non-Sequential])  

Settings.json
```
{
    "station_name": "kwb",
    "subtitles:": "true",
    "file_location": "",
    "playlist_location": "",
    "use_external_playlist": "http://blahblah:3k/myplaylist.m3u8"
} 
```

Setting file location will cause all file references in ScheduleTemplate.json to be prefix by it:
"file_location" + "location"
Leaving this to default will cause the schedule desinger to look for an external drive

playlist_location tells the scheduler where to save the schedules, and the player where to read the schedule from.

Already have an external playlist? use_external_playlist will override the scheduler and play that network stream.

ScheduleTemplate.json
```
{
     "default" : {
        "start_time": 8,
        "end_time": 18,
        "schedule_items": [
            {"location": "/foldername", "tags": ["block1"], "content": "ns"},
            {"location": "/foldername", "tags": ["block1"]},
            {"location": "/foldername", "tags": ["block1", "block3"]},
            {"location": "/foldername", "tags": ["block1", "block3"]},
            {"location": "/foldername", "tags": ["block2"], "content": "ns"},
            {"location": "/foldername", "tags": ["block2"], "content": "ns"},
            {"location": "/foldername", "tags": ["block2"], "content": "ns"},
            {"location": "/foldername", "tags": ["block3"]}
        ],
        "schedule": {
            "block1": {
                "start": 8,
                "end": 11
            },
            "block2": {
                "start": 11,
                "end": 15,
                "allowed-content": ["ns"]
            },
            "block3": {
                "start": 15,
                "end": 18
            },
            "block4": {
                "start": 18,
                "end": 20
            }
        },
        "bumpers": "./foldername",
        "commercials": "./foldername"
    },
    "saturday" : {},
    "sunday" : {}
}
```

The default option can be used as a backup in case a specific day of the week is not specified.
Shows can be re-used for multiple blocks via tags.

Blocks have their times, and content can be locked down to specific content types, 
:"ns" - non-sequential, these are shows that it does not matter what order they are played in. specifying ns will make the show play in random order.
:"s" 

 We want a schedule like

 ```
| Tv show 1 | Bumpers/Commercials | Tv show 2 |  Bumpers/Commercials | Tv show 3 |... Etc
 ```

The idea box of wants:
```
A Concept of weekly new releases?
Staggered syndication?
Reruns
We want to make sure that the first episode of tv show 1 happens sequentially before the episode shown in the first slot.

```


## Program layout

### Setup.sh
    Creates a cron job that runs the scheduler every day to generate a playlist :-)

### Shedule Designer
    This handles creating the playlists for the day

### Player
    This handles starting up vlc and running the playlists