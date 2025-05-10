# Nexus Appointment Notifier

A Python script that continuously checks for available Nexus/Global Entry interview appointments and alerts you when one becomes available within your specified timeframe.

## Features

- Monitor multiple enrollment center locations simultaneously
- Specify a timeframe (hours, days, or months) or exact date range
- Customizable checking interval
- Audio alerts when appointments are found
- Simple command-line interface

## Requirements

- Python 3.6+
- Required Python packages:
  - `requests`
  - `python-dateutil`
  - `playsound`

## Installing Python

Before installing the required packages, you need to have Python installed on your system:

### Windows
1. Download the latest Python installer from [python.org](https://www.python.org/downloads/)
2. Run the installer and make sure to check "Add Python to PATH" during installation
3. Verify installation by opening Command Prompt and typing: `python --version`

### macOS
1. Option 1: Download from [python.org](https://www.python.org/downloads/)
   - Run the installer and follow the instructions
2. Option 2: Using Homebrew (recommended if you have Homebrew installed)
   - Open Terminal and run: `brew install python`
3. Verify installation by opening Terminal and typing: `python3 --version`

### Linux
1. Most Linux distributions come with Python pre-installed
2. If not, install using your distribution's package manager:
   - Ubuntu/Debian: `sudo apt update && sudo apt install python3 python3-pip`
   - Fedora: `sudo dnf install python3 python3-pip`
   - Arch Linux: `sudo pacman -S python python-pip`
3. Verify installation by opening Terminal and typing: `python3 --version`

## Installation

1. Clone this repository or download the `main.py` file
2. Install the required packages:

```bash
# For systems where Python 3 is accessed via 'python3' command:
pip3 install requests python-dateutil playsound
# OR
pip3 install -r requirements.txt

# For systems where Python 3 is the default 'python' command:
pip install requests python-dateutil playsound
# OR
pip install -r requirements.txt

# Alternative method (works on all systems):
python3 -m pip install -r requirements.txt
```

3. Place an audio file (e.g., `alarm.mp3`) in the same directory as the script

## Usage

### Basic Usage

Run the script with default settings (checks Blaine, WA Nexus location [ID: 5020] for the next 6 months):

```bash
# If your system uses 'python3' command:
python3 main.py

# If your system uses 'python' command for Python 3:
python main.py
```

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--locations` | `-l` | List of location IDs to check (default: 5020 - Blaine, WA) |
| `--timeframe` | `-t` | Timeframe to check (e.g., "24h", "7d", "3m") (default: 6m) |
| `--date-range` | `-d` | Specific date range (format: YYYY-MM-DD YYYY-MM-DD) |
| `--interval` | `-i` | Check interval in seconds (default: 3) |
| `--sound` | `-s` | Path to sound file (default: alarm.mp3) |

### Examples

Check multiple locations:
```bash
python3 main.py -l 5020 5140 5142
```

Check for appointments in the next 24 hours:
```bash
python3 main.py -t 24h
```

Check for appointments in a specific date range:
```bash
python3 main.py -d 2023-12-01 2024-02-28
```

Check every 10 seconds:
```bash
python3 main.py -i 10
```

Use a custom sound file:
```bash
python3 main.py -s /path/to/custom_sound.mp3
```

Combine multiple options:
```bash
python3 main.py -l 5020 5140 -t 3m -i 5 -s notification.mp3
```

> **Note:** If your system uses `python` as the command for Python 3 (common on Windows or in virtual environments), replace `python3` with `python` in the examples above. Similarly, use `pip` instead of `pip3` for package installation.

## Stopping the Script

Press `Ctrl+C` in your terminal to stop the script.

## License

This project is open source and available under the MIT License.