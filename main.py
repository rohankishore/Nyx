import cv2
import sys
import os
import questionary
import time
from ffpyplayer.player import MediaPlayer
#from pytube import YouTube
import downloadVid #local import that download the video

#------------------------
#If you don't want to download the video, comment out 7th line 
# and change the path to the video you want to use on line 36
#------------------------

#To Add
#Multithread
#Cleanup
#Use background color as an option
#Option for flipped colors, looked cool
#Remake in rust

# ·  ·  ·  ·  #

ASPECT_RATIO = 1.5 #Ratio of height to width for font

palletes = {
    "Regular": ["#", "%", "?", "+", ":", "·", "·"],
    "Inverse": ["·", "·", ":", "+", "%", "#", "#"],
    "\"Monochrome\"": ["#", "·", "·"]
}

modes = {
    "Use max terminal space": 2,
    "Maintain aspect ratio": 1,
}

display_modes = [
    "YouTube",
    "Local file"
]

#Might still be messy
ascii_choice = questionary.select(
    "What ASCII scheme to use ? (Try the other options if video looks bad)",
    choices=list(palletes.keys()),
    ).ask()
ascii_scheme = palletes[ascii_choice]

mode_choice = questionary.select(
    "Which do you prefer ? (If one breaks, pick the other)",
    choices=list(modes.keys())
).ask()
mode = modes[mode_choice]

display_choice = questionary.select(
    "Would you like to play a video from YouTube or a local file ?",
    choices=display_modes
).ask()

path = None
if display_choice == display_modes[0]:
    # Input video url
    video_url = input("[*]Enter video URL: ")

    #Downloads video, returns path to file
    path = downloadVid.download_video(video_url)
else:
    path = questionary.text("Then what is the path to your video ?",).ask()

#Set video source
video = cv2.VideoCapture(path)
player = MediaPlayer(path)

def grayscale(rgb):
    rgb = rgb
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    brightness = (r + g + b) / 3
    return brightness

def print_frame(img, frame_time):
    current_time = time.time()
    #Take image, turn greyscale, resize

    #Find maximum number of characters based on terminal size
    #Check terminal size in loop to be fancy
    terminal = os.get_terminal_size()
    term_width = terminal.columns
    term_height = terminal.lines

    #Needs to be even to center neatly
    if term_width % 2 != 0:
        term_width -= 1

    height = img.shape[0]
    width = img.shape[1]
    #How much width per height for original to keep aspect ratio
    original_ratio = width / height

    width_ratio = term_width / width
    height_ratio = term_height / height

    if mode == 1:
        # Maintain aspect ratio - fit to terminal height
        new_height = term_height - 2  # Leave space for top/bottom
        new_width = int(new_height * original_ratio / ASPECT_RATIO)
        # Ensure it fits within terminal width
        if new_width > term_width:
            new_width = term_width
            new_height = int(new_width * ASPECT_RATIO / original_ratio)
        small_img = cv2.resize(img, (new_width, new_height))
    elif mode == 2:
        # Use max terminal space
        small_img = cv2.resize(img, (0, 0), fx=width_ratio, fy=height_ratio)

    #Find how much needs to be cleared every new frame
    small_height = small_img.shape[0]
    small_width = small_img.shape[1]

    #How much of the brightness each character occupies
    magic_num = 255/(len(ascii_scheme)-1.001)
    #This does the actual job
    ascii = ""
    for col in small_img:
        size_difference = term_width - small_width

        if size_difference > 1:
            for i in range(int(size_difference/2 + 1)):
                ascii += " "

        for row in col:
            brightness = grayscale(row)
            character = ascii_scheme[int(brightness // magic_num)];
            ascii += f'\x1b[38;2;{row[2]};{row[1]};{row[0]}m{character}'
        ascii += "\n"

    print(ascii[:-1], end="\033[0m")  # Reset ANSI formatting
    
    # Calculate sleep time to maintain frame rate
    elapsed = time.time() - current_time
    sleep_time = max(0, frame_time - elapsed)
    if sleep_time > 0:
        time.sleep(sleep_time)
    
    sys.stdout.write(f"\033[{small_height + 1}F")  # Cursor up n lines

fps = video.get(cv2.CAP_PROP_FPS)
print(f"FPS is {fps}")
frame_time = 1 / fps

# Start timing from first frame
start_time = time.time()
frame_count = 0

while True:
    success, image = video.read()
    
    if not success:
        break
    
    # Calculate expected time for this frame
    frame_count += 1
    expected_time = start_time + (frame_count * frame_time)
    current_time = time.time()
    
    # Skip frames if we're behind schedule
    if current_time > expected_time + frame_time:
        continue
    
    print_frame(image, frame_time)
    
    # Keep audio playing
    audio_frame, val = player.get_frame()

print("\n\nVideo finished!")