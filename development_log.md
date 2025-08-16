# Log

Here is a log of all my thoughts...

## Controlling VLC

We want to build a playlist from a scheduling template, then load that playlist into vlc

python-vlc is what we are going to be using to facilitate 

We can load a playlist from the cmd line

Or we can use python-vlc to programatically handle it:

``` python
# media object
media = vlc.Media("1mp4.mkv")


# setting media to the media player
media_player.set_media(media)
```

While running the player we can check if the playlist is still playing via: .is_playing()
``` python
While .is_playing():
```

So now we need to worry about scheduling

* side note: 
    Maybe a better version of this may be to use mpv a la; from python_mpv_jsonipc import MPV?
    I am seeing a ton of conflicting info around mpv so I am gonna stick with vlc for this project.

## Generating a schedule

We need to generate a dynamic schedule for a (day || week)

using kwb as an example, their schedule was something like
8-11a.m. (3 hours or 6 episodes)
-- We can figure out how to stick a we'll be back message here, or just fill it with random non-sequential episodes or reruns of the previous block
11-3p.m. (4 hours or 8 episodes [Reruns][Non-Sequential])
3-5p.m. (2 hours or 4 episodes)
5-8p.m. (3 hours 6 episodes [Reruns][Non-Sequential])  

Settings.json
``` json
{
    "station_name": "kwb",
    "subtitles:": "true",
    "file_location": "",
    "playlist_location": ""
} 
```

Setting file location will cause all file references in ScheduleTemplate.json to be prefix by it:
"file_location" + "location"
Leaving this to default will cause the schedule desinger to look for an external drive

playlist_location tells the scheduler where to save the schedules, and the player where to read the schedule from.

Already have an external playlist? use_external_playlist will override the scheduler and play that network stream.

ScheduleTemplate.json
``` json
{
     "default" : {
        "start_time": 8,
        "end_time": 18, // if this is -1 we stop at the start time?
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
| Tv show 1 | bumper| Commercials | bumper | Tv show 2 | bumper| Commercials | bumper | Tv show 3 |... Etc
 ```

The idea box of wants:
```
A Concept of weekly new releases?
Staggered syndication?
Reruns
We want to make sure that the first episode of tv show 1 happens sequentially before the episode shown in the first slot.
```

### Actually generating the M3U8 Playlists

https://en.wikipedia.org/wiki/M3U


linux pathing for playlist
```
file:///media/{login_name}/{drive_name}/{file_name}
```

## Trials and Tribulations

The very first issue I ran into in this project was that by default the RPI4 is not setup to display an analog signal, this took a bit of research to figure out and there were a ton of 
videos and forums that I had to peruse to find the final correct answer. see the section above on how to setup ;-)

The next issue I ran into is that python_vlc operates differently than I would have expected when compared to VLC player. the library uses two different media players when working with one video vs a playlist.
This was troublesome because the media_list_player that the lib provides is technically a wrapper that does not give you direct access to things like options for full screen and moving to a specific time in the play list. This was trivial when calling vlc through the cmd line,  `vlc --playlist /path/to/your/playlist.m3u --start-time=seconds`, this would start your playlist at the specific time that matched in the list and video. Which would have made it trivial to start the server at a specific time. In order to fix this I wound up having to add each item to the playlist individually. :-/ 

A second issue cropped up around this, If the scheduler needs to crop a video there is no way to organically do this with a m3u8 playlist. You can tell anything reading the playlist where to start and how long each segment should be at the max but you cannot do it per file. Luckily the solution I came up with for the prior issue also helped solve this. I added two new properties `#x-start:10, #x-end:30` to my scheduler that will allow it to specify where in the video to start and where to end. 

Getting this to work with the scheduler turned out to be a monumental task.

Orchestration - this is a big issue, how to I make sure each pi is playing and how do I ensure that the stream starts on time?
The answer, I am just going to run it with the server
All config setup can be done through the server, and I expect it to be running at all times.
I will just create a call back that runs every so often and calls the scheduler as a sub process. I have the scheduler only set to create schedules for a 7 day period and it should not run over itself.

### vlc freezing

Randomly vlc would just stop playing when trying to move onto the next item in the playlist, it took a long time to diagnose this because of the infrequency of the issue. It turns out the issue was with the external drive and how it was connected to the pi. I had it connected via the old school usb ports and this was causing some latency when retrieving the files.

### Auto start and why I hate linux

since we are using vlc we need to run this when the desktop is started and the user is logged in.
I accomplished this through .Desktop files in /.config/autostart,, why did this need to be so hard!

```
update pibro.desktop to point at your instalation
update pibro.sh to match your setup (I have a network mount that I included)
copy scripts/pibro.desktop to ~/.config/autostart
reboot your pi
profit
```

# vlc is still freezing, WHY!!!?!
Oh thats why! turns out vlc and the pi hates x-lib.

# Oh cool now the usb drive randomly disconnects
This sucks, it turns out the usb ports on the pi are not strong enough to handle a 2.5" external drive, I am now using folder sharing from a laptop and connecting via smb
So far all good!

# Now my schedule syncing is not working....
I am relying on vlc to stop the video at a specific time..., this should lead to videos landing on 00:15, 00:30, or 1:00 marks. However, after a few hours we lose sync by a few minutes...
I am not sure why. I need to parse the schedule files and see if I can find the issue... 

# I aint using no stinkin cron
I wanted to make this app universal, so I have decided to do the auto scheduler in code. It works!

# STREEEEEAMING
Added a stream player! 
Here are some of my favorites!
- https://swimrewind.com/
- http://api.toonamiaftermath.com:3000/est/playlist.m3u8

Basically any network streams vlc can handle can be used with pibroadcast!
I think technically you could probably setup your own owncast setup and use it?

# BUGS
Every time I squash one another pops up.
1. Killed a bug resulting in shows start times drifting. Turns out you cant just cut milliseconds off of shows and expect them to end correctly.
2. Murderlated a bug that made it to where the first show would never start... Turns out negative time exists....

# Why is it so hard to get swagger setup for flask...
