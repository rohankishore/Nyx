<p align="center">
  • • •
</p>

<h1 align="center">NYX</h1>

<p align="center">
  terminal ascii video player<br>
  light reduced to symbols
</p>

<p align="center">
  • • • • •
</p>

---

### • what is nyx

**nyx** is a terminal-based video player that renders videos frame-by-frame  
using **ASCII symbols** and **true-color ANSI output**.

it supports:
• local video files  
• youtube videos  
• audio playback  
• adaptive terminal resizing  

nyx works best in darkness.

---

### • how it works

• reads video frames using **opencv**  
• converts pixels to brightness  
• maps brightness to ascii characters  
• renders frames using **24-bit ANSI colors**  
• syncs audio using **ffpyplayer**  

every frame is redrawn inside your terminal.

---

### • ascii palettes

nyx supports multiple ascii rendering styles:

• **regular** — balanced contrast  
• **inverse** — dark-first visuals  
• **monochrome** — extreme minimalism  

choose the one that fits your video.

---

### • display modes

• **maintain aspect ratio**  
• **use maximum terminal space**  

nyx automatically adapts to your terminal size.

---

### • supported sources

• local video files  
• youtube links (auto-download)  

---

### • requirements

• python 3.9+  
• opencv  
• ffpyplayer  
• pytube  
• questionary  

install dependencies:

```bash
pip install opencv-python ffpyplayer pytube questionary
