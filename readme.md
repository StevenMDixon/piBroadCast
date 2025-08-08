# piBroadCast

piBroadCast is a attempt at making a simple but effect home broadcast solution. This solution should be scalable and each pi will act as an individual station, programmed with old commercials and bumpers!

I would like to give credit for my inspiration around this project to Shane Mason, his work on FieldStation42 is amazing and you should check it out if you want a more feature rich solution.
https://github.com/shane-mason/FieldStation42/tree/main

## Why, tho?

I wanted to be able to play old media across my home via coaxial cables. Obviously going through my mid-life crisis here :-)

I also wanted to have a strict control over what is being seen by my child, without potentially giving them access to the internet. And retain the ability to cut it off if need be :Devil


## The Ideal setup (mine)

The plan is to use 4 Raspberry pi's being piped into a `Channel Plus Box Model 5545 Quad Digital Modulator` that will result in any tv in the house being able to pickup 4 channels that are specified from the QuadRF

```
Pi 1 ______
Pi 2 ______|               
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
dtoverlay=
```

Then add this anywhere
```
enable_tvout=1
sdtv_mode=0
sdtv_aspect=4:3
```
This will disable hdmi out, you can try autodetect but i found it is not reliable

sdtv_mode = 0 is for NTSC, there a ton of other modes to choose from check the official docs for those values

In cmdline.txt add this to the end

```
video=Composite-1:720x480@60ie
```

you can add `,margin_left=40,margin_right=40,margin_top=32,margin_bottom=32` to the end of the line above but it will have negative effects on vlc

You may need to edit your margins. YMMV.

Also depending on your composite cables red and yellow may be swapped.

If you are planning on connecting the pis to other network items make sure to set the hostname!

If you are planning on running media from an attached drive/usb, make sure to go into File_manager -> edit -> preference -> volumn management and deselect show available options.. Otherwise everytime you swap in a new drive you will get a popup


## Program layout

### Setup.sh
    Sets up venv and installs packages

### scheduler_sub
    This handles creating the playlists, this can be run as a standalone program but is meant to be called from the server

### player_sub
    This handles starting up vlc and running the playlists

### server
    Creates an API that allows control over what the pi and allows you to setup config remotely

## Template config

## Station config