# 🦆 DuckyRecorder v1.0.0

![DuckyRecorder Menu](docs/menu.png)

DuckyRecorder is a CLI tool for recording HID events (keyboard and mouse) and exporting interactions into formats compatible with USB HID devices such as Rubber Ducky and ATmega32u4-based boards.

> ⚠️ Restricted to authorized environments, security testing with explicit permission, and legitimate automation.

---

## ✨ Features

* 🎙️ **Real-time recording** – Captures keyboard and mouse events with precise timestamps
* ⏯️ **Smart control** – Pause/resume with configurable hotkeys (F9/F10 by default)
* 👁️ **Live preview** – Displays captured events in real time during recording
* 💾 **Structured storage** – Saves recordings in JSON format with metadata
* 📤 **Multi-platform export** – Converts to:

  * Rubber Ducky (`.ducky.txt`)
  * Arduino HID (`.ino`) with `Keyboard.h` and `Mouse.h` support
* 🌍 **Internationalization** – Portuguese and English support
* 🎨 **Rich CLI interface** – Colors, adaptive banners, and interactive menus
* ⚙️ **Persistent configuration** – Settings automatically saved in JSON
* 🔧 **Logging system** – Detailed logs for debugging and monitoring
* 🖱️ **Precise mouse control** – Relative movement, clicks, and optional cursor reset

---

## 📁 Project Structure

```text
DuckyRecorder/
├── DuckyRecorder/
│   ├── cli/
│   ├── core/
│   │   ├── colors.py
│   │   ├── events.py
│   │   ├── hotkeys.py
│   │   ├── language.py
│   │   ├── recorder.py
│   │   └── timeline.py
│   ├── exporters/
│   │   ├── ducky.py
│   │   └── arduino.py
│   ├── utils/
│   │   ├── console.py
│   │   └── logger.py
│   ├── config/
│   ├── lang/
│   ├── __init__.py
│   ├── main.py
│   └── __main__.py
├── config/
├── recordings/
├── exports/
├── logs/
├── docs/
│   └── menu.png
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🛠️ Installation

### Requirements

* Python 3.8+
* pip

### Step by step

```bash
git clone https://github.com/your-username/DuckyRecorder.git
cd DuckyRecorder
pip install -r requirements.txt
```

### Dependencies

* `pynput>=1.7.6`
* `colorama>=0.4.6`

---

## ▶️ Usage

### Run

```bash
python -m DuckyRecorder
# or
python DuckyRecorder/main.py
```

### Typical workflow

1. Start recording
2. Perform actions (typing, clicks, etc.)
3. Stop recording (F10 by default)
4. Export to the desired format
5. Use the exported file in an authorized environment

---

## 📦 Export Formats

### 1️ Rubber Ducky (`.ducky.txt`)

* Converts text to `STRING`
* Preserves `DELAY`
* Groups consecutive characters
* Comments unsupported events

### 2️ Arduino HID (`.ino`)

Compatible with:

* Arduino Leonardo
* Arduino Micro
* Pro Micro
* ATmega32u4

Features:

* `Keyboard.print()` for text
* `Keyboard.press()` / `Keyboard.release()` for special keys
* `Mouse.move()` with automatic segmentation
* Left, right, and middle clicks
* Optional initial cursor reset

---

## ⚙️ Configuration

File: `config/config.json`

```json
{
  "language": "pt",
  "mouse_speed": "FAST",
  "zero_mouse_on_start": true,
  "auto_save": true,
  "pause_key": "F9",
  "stop_key": "F10",
  "default_recording_name": "",
  "show_live_preview": true,
  "max_events_display": 10
}
```

---

## 🔐 Ethical Use

This tool must be used exclusively for:

* Personal environments
* Authorized testing
* Research and study
* Legitimate automation
* Accessibility purposes

Misuse may violate local laws and institutional policies.

---

## 🐛 Logs

* Real-time logs in the menu
* Persistent files in `logs/`
* Levels: DEBUG, INFO, WARNING, ERROR
* Automatic rotation (up to 1000 messages in memory)

---

## 🧠 Future Roadmap

* Automatic local replay
* Advanced event filters
* Visual timeline editor
* Export plugins
* REST API
* Additional language support

---

## 📄 License

MIT License

Copyright (c) 2026 MarllonDevSec

---

## 🤝 Contributing

1. Fork
2. Create a branch
3. Commit
4. Push
5. Open a Pull Request

---

## 🏗️ Architecture

### Recorder

Handles listeners and event capturing.

### Timeline

Manages temporal sequencing and event normalization.

### Exporters

Transform events into specific output formats.

### Language Manager

Dynamic language loading system.

### Config Manager

Configuration persistence and automatic merging system.
