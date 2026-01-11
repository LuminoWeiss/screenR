# Screen Recorder

A Python-based screen recorder with easy-to-use command-line interface and multiple termination options.

## Features

- **Easy Parameter Input**: Command-line arguments for duration, filename, resolution, and FPS
- **Multiple Stop Options**:
  - Press `q` in the preview window
  - Press `ESC` key (works globally)
  - Press `Ctrl+C` in terminal
- **Real-time Preview**: See what you're recording in a resizable window
- **Progress Tracking**: Live countdown showing elapsed and remaining time
- **Auto-generated Filenames**: Timestamps added automatically if no filename specified
- **Recording Summary**: Shows total duration, frames recorded, and output location

## Installation

Install required dependencies:

```bash
pip install pyautogui opencv-python numpy pynput
```

## Usage

### Basic Usage

Record for 60 seconds with default settings:
```bash
python s_recorder.py -d 60
```

### Specify Custom Filename

```bash
python s_recorder.py -d 120 -f my_presentation.avi
```

### Full Custom Recording

```bash
python s_recorder.py --duration 300 --filename demo.avi --resolution 1920x1080 --fps 60
```

### Command-Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--duration` | `-d` | Recording duration in seconds | 3600 (1 hour) |
| `--filename` | `-f` | Output filename | `recording_TIMESTAMP.avi` |
| `--resolution` | `-r` | Screen resolution (WIDTHxHEIGHT) | `1920x1080` |
| `--fps` | | Frames per second | `30.0` |

### View Help

```bash
python s_recorder.py --help
```

## Stopping the Recording

You have three options to stop recording before the time limit:

1. **Press `q`** - While the preview window is in focus
2. **Press `ESC`** - Works globally, even when the preview window isn't focused
3. **Press `Ctrl+C`** - In the terminal where the script is running

## Examples

### Quick 30-second test recording
```bash
python s_recorder.py -d 30 -f test.avi
```

### High-quality 5-minute presentation
```bash
python s_recorder.py -d 300 -f presentation.avi --fps 60
```

### 2K resolution recording
```bash
python s_recorder.py -d 600 -r 2560x1440 -f demo_2k.avi
```

## Output

During recording, you'll see:
```
============================================================
Recording started!
Duration: 60 seconds (1.0 minutes)
Output file: my_recording.avi
Resolution: 1920x1080 @ 30.0 FPS
============================================================
Press 'q' in the preview window or ESC to stop recording
============================================================

Recording... 45s / 60s (15s remaining)
```

After recording, you'll get a summary:
```
============================================================
Recording stopped!
Total duration: 60.0 seconds (1.0 minutes)
Total frames: 1800
Output saved to: my_recording.avi
============================================================
```

## Notes

- The output file format is AVI with XVID codec
- The preview window can be resized as needed
- Recording will automatically stop when the duration is reached
- Filenames without `.avi` extension will have it added automatically
