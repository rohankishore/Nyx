import cv2
import sys
import os
import questionary
import time
from ffpyplayer.player import MediaPlayer
from pytube import YouTube
import ytDl

def show_nyx_banner():
    nyx = [
        "███╗   ██╗██╗   ██╗██╗  ██╗",
        "████╗  ██║╚██╗ ██╔╝╚██╗██╔╝",
        "██╔██╗ ██║ ╚████╔╝  ╚███╔╝ ",
        "██║╚██╗██║  ╚██╔╝   ██╔██╗ ",
        "██║ ╚████║   ██║   ██╔╝ ██╗",
        "╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝"
    ]

    colors = [
        196, 202, 208, 214, 220, 226,
        190, 154, 118, 82, 46, 47,
        48, 49, 51, 45, 39, 33
    ]

    os.system("cls" if os.name == "nt" else "clear")

    for i, line in enumerate(nyx):
        color = colors[i % len(colors)]
        print(f"\033[38;5;{color}m{line}\033[0m")

    print("\n\033[38;5;245m• terminal ascii video player •\033[0m\n")
    time.sleep(0.8)


ASPECT_RATIO = 1.5

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

show_nyx_banner()
ascii_choice = questionary.select(
    "Pick an ASCII style (if it looks weird try another one)",
    choices=list(palletes.keys()),
    ).ask()
ascii_scheme = palletes[ascii_choice]

mode_choice = questionary.select(
    "Pick display mode (if one breaks just try the other)",
    choices=list(modes.keys())
).ask()
mode = modes[mode_choice]

display_choice = questionary.select(
    "YouTube video or local file?",
    choices=display_modes
).ask()

path = None
if display_choice == display_modes[0]:
    video_url = input("paste youtube link: ")
    path = ytDl.download_video(video_url)
else:
    path = questionary.text("path to your video?",).ask()

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
    terminal = os.get_terminal_size()
    term_width = terminal.columns
    term_height = terminal.lines

    if term_width % 2 != 0:
        term_width -= 1

    height = img.shape[0]
    width = img.shape[1]
    original_ratio = width / height

    width_ratio = term_width / width
    height_ratio = term_height / height

    if mode == 1:
        new_height = term_height - 2
        new_width = int(new_height * original_ratio / ASPECT_RATIO)
        if new_width > term_width:
            new_width = term_width
            new_height = int(new_width * ASPECT_RATIO / original_ratio)
        small_img = cv2.resize(img, (new_width, new_height))
    elif mode == 2:
        small_img = cv2.resize(img, (0, 0), fx=width_ratio, fy=height_ratio)

    small_height = small_img.shape[0]
    small_width = small_img.shape[1]

    magic_num = 255/(len(ascii_scheme)-1.001)
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

    print(ascii[:-1], end="\033[0m")
    
    elapsed = time.time() - current_time
    sleep_time = max(0, frame_time - elapsed)
    if sleep_time > 0:
        time.sleep(sleep_time)
    
    sys.stdout.write(f"\033[{small_height + 1}F")

fps = video.get(cv2.CAP_PROP_FPS)
print(f"fps: {fps}")
frame_time = 1 / fps

start_time = time.time()
frame_count = 0

while True:
    success, image = video.read()
    
    if not success:
        break
    
    frame_count += 1
    expected_time = start_time + (frame_count * frame_time)
    current_time = time.time()
    
    if current_time > expected_time + frame_time:
        continue
    
    print_frame(image, frame_time)
    
    audio_frame, val = player.get_frame()

print("\n\ndone!")