<p align="center">

<img width="332" height="150" alt="nyx-banner" src="https://github.com/user-attachments/assets/f727555e-6437-4e90-9ba1-22d508e47206" />

</p>

<p align="center">
  terminal ascii video player<br>
  light reduced to symbols
</p>

---

## • WTF is Nyx?

![deadpool - Trim](https://github.com/user-attachments/assets/f9e05f6d-38ab-4b4a-81e7-b69e3af167fe)


**Nyx** is a terminal-based video player that renders videos frame-by-frame  
using **ASCII symbols** and **true-color ANSI output**.

it supports:
• local video files  
• youtube videos  
• audio playback  
• adaptive terminal resizing  

Nyx works best in darkness.

---

## • Usage

```bash
python main.py
```


---

## • How it Works

• reads video frames using **opencv**  
• converts pixels to brightness  
• maps brightness to ascii characters  
• renders frames using **24-bit ANSI colors**  
• syncs audio using **ffpyplayer**  

every frame is redrawn inside your terminal.

---

## • ASCII Palettes

nyx supports multiple ascii rendering styles:

• **regular** — balanced contrast  
• **inverse** — dark-first visuals  
• **monochrome** — extreme minimalism  

choose the one that fits your video.

---

## • Display Modes

• **maintain aspect ratio**  
• **use maximum terminal space**  

Nyx automatically adapts to your terminal size.

  > [!TIP]
  > Use the Terminal in Full Screen for the best results

---

## • Supported Sources

• local video files  
• youtube links (auto-download)  

---

## • Requirements

install dependencies:

```bash
pip install -r requirements.txt
```
