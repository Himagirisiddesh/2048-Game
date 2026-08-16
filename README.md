<div align="center">

# 🎮 2048 Game — Advanced Pygame Edition

**A visually enhanced, feature-rich take on the classic 2048 game, built with Python & Pygame.**

Goes well beyond the basic game with a modern UI, particle effects, a fully procedural audio system, and smooth animations throughout.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-game%20engine-brightgreen?logo=python&logoColor=white)](https://www.pygame.org/)
[![Architecture](https://img.shields.io/badge/Architecture-OOP%20%2B%20Game%20Loop-blueviolet)](#)
[![Audio](https://img.shields.io/badge/Audio-Procedural%20Synthesis-orange)](#-audio-system)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#-license)

</div>

---

## ✨ Features

### 🕹️ Core Gameplay
- Classic 4×4 grid-based mechanics
- Tile merging with score tracking
- Win condition at the 2048 tile
- Full game-over detection

### 🎨 Advanced UI/UX
- Smooth tile-movement animations
- Dynamic scaling and pulse effects
- Gradient backgrounds with glowing panels
- Interactive buttons with hover and press effects

### 🔊 Sound Effects System
- Fully **procedural audio generation** — no external sound files
- Distinct feedback for: move, merge, spawn, win/lose, and button clicks

### 💥 Visual Effects
- Particle explosion on tile merge
- Floating score popups
- Animated background motion
- Win-celebration effects

### 📊 Score System
- Real-time score tracking
- Persistent best score, saved locally

### 🖥️ Responsive Design
- Resizable game window
- Adaptive board scaling

## 🧩 Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Library | Pygame |
| Architecture | OOP + game loop |
| Audio | Procedural synthesis |

## 📁 Project Structure

```
2048-Game/
├── 2048_gmae.py       Main game script
├── best_score.txt      Persistent best-score storage
└── README.md
```

## ▶️ How to Run

### 1 · Install dependencies

```bash
pip install pygame
```

### 2 · Run the game

```bash
python 2048_gmae.py
```

## 🎮 Controls

| Key | Action |
|---|---|
| ⬅️ | Move left |
| ➡️ | Move right |
| ⬆️ | Move up |
| ⬇️ | Move down |
| `R` | Restart game |
| 🖱️ Mouse | UI interactions |

## 🧠 Game Logic Overview

- The board is represented as a 2D 4×4 grid
- Tiles slide in the selected direction
- Matching tiles merge into their combined value
- After each move, a new tile (`2` or `4`) spawns at random
- The game ends when there are no empty cells **and** no possible merges

## 🔊 Audio System

Instead of external audio files, this project uses a **procedural sound engine** that generates effects on the fly using:

- Sine waves
- Frequency modulation
- Exponential decay

**Why it matters:** lightweight, fully self-contained, and technically more interesting than shipping static `.wav` files.

## 🎨 UI Highlights

- Gradient background rendering
- Glass-like tile design
- Glow effects around the best score
- Animated overlays for 🏆 win and ❌ game-over states

## 📈 Future Improvements

- 🔢 Larger grid sizes (5×5, 6×6)
- ↩️ Undo functionality
- 🌐 Leaderboard system
- 📱 Mobile/touch support
- 🤖 AI auto-play mode

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 🙌 Author

**Himagiri Siddesh M**

## ⭐ Show Your Support

If you like this project:
⭐ star the repo · 🍴 fork it · 📢 share it

---

<div align="center">
Built with Python and Pygame
</div>
