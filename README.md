# CodeQuest: Space Adventure 🚀

![Made with Python](https://img.shields.io/badge/Python-3.10+-blue)
![Kids Friendly](https://img.shields.io/badge/Kids%20Project-Yes-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

A fun **Python Turtle** game for kids: move your spaceship, collect stars, and dodge meteors!

## 🎮 Features
- 3 lives, with a rising difficulty as your score grows
- Collect stars to raise your score; dodge falling meteors
- Occasional blue shield power-up
- High score saved to `high_score.txt` in the working directory
- Simple, kid-friendly code structure

## 🎛 Controls
- **← / →** (Left / Right arrow keys): move the ship horizontally
- **SPACE**: start the game, or restart after Game Over

## ▶️ Run Locally

Clone the repo and run from the **repository root** (sprite paths are relative to the cwd):

```bash
git clone https://github.com/pranjulya/CodeQuest-Space-Adventure.git
cd CodeQuest-Space-Adventure
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/game.py
```

**Linux note:** Turtle needs Tk. If you see errors about `_tkinter` or a missing display, install it first, e.g. `sudo apt install python3-tk`.

`high_score.txt` is written next to where you launch the game and is listed in `.gitignore`.
