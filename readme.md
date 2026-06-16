# Rod-and-Disk Stimulus Presentation

## Overview

This is a pygame application to run the classic rod-and-disk task. In each trial, the participant uses the mouse wheel to align a central rod to perceived vertical, while peripheral vision is occupied by static or rotating dots. The application features customizable and reproducible stimulus generation and CSV data logging. 

## Installation

### Windows 11

- <a href="https://yiling-huo.github.io/files/programs/rod-and-disk-python.zip" download>Download (Windows 11, 64-bit)</a>.
- Running on Windows 11:
    - After downloading, extract the ZIP and run `rod-and-disk-python.exe`.
    - If Windows SmartScreen shows a “Windows protected your PC” warning:
        - Click “More info”.
        - Click “Run anyway”.
        - *Optional: to avoid repeated warnings, right-click the downloaded file, choose Properties, check “Unblock”, then Apply*.

### Other systems / Source code

- Python: 3.10 - 3.13 recommended.
- Dependencies:
    - pygame >= 2.6.0 (Install via pip: `pip install pygame`)
    - tkinter (ships with most Python distributions; on Linux, install system package e.g., `apt-get install python3-tk`)
- Running
    - From a terminal: `python rod_and_disk.py`
    - The program opens in exclusive fullscreen on the primary display. The mouse cursor is hidden during the task.

## Main features

- GUI setup dialog for all experiment and appearance parameters.
- Pre-built rotated disk frames for smooth rotation at 60 fps.
- Reproducible dot layouts and trial start angles via a single randomization seed.
- Double-press ESC safe-exit with on-exit data write.

## Controls (during task)

- ENTER: start the experiment from the instruction screen.
- SPACE: advance to the next trial.
- Double-press ESC (within 500 ms): save collected data and quit.
- Mouse wheel: rotate rod.

## Customizable fields

### Experiment parameters

- Participant ID: free text (required).
- Condition: motion or static.
- Number of trials: positive integer.
- Rod beginning angle (+/−): starting offset from vertical in degrees; applied as ±angle per trial.
- Rod velocity (deg/input): degrees per mouse-wheel unit (0–360, exclusive of 0).
- Disk rotation direction: clockwise or counterclockwise (ignored if static).
- Disk rotation speed (deg/s): ≥ 0 (ignored if static; recorded as N/A).
- Randomisation seed: integer, up to 20 digits; governs dot layout and sign of rod start angle per trial.

### Appearance parameters
*You should keep these consistent within an experiment.*
- Disk count: number of dots generated on the canvas. *Note: canvas side length equals the screen diagonal, so not all dots are necessarily visible at once.*
- Rod length (pixels): the length of the rod.
- Central radius (pixels): the radius of the no-dot central window. *Should be larger than rod length.*
- Disk diameter (pixels): the diameter of each dot.
- Minimum gap between disks (pixels)

### Data logging

- Location: `results/{ParticipantID_YYYYMMDD_HHMMSS}.csv`
- Columns:
    1. Date
    1. Time
    1. Trial Start Time (ms; pygame ticks)
    1. Trial End Time (ms; pygame ticks)
    1. Randomisation seed
    1. Participant
    1. Condition
    1. Trial
    1. Trial Duration (ms)
    1. Rod Start Position (deg)
    1. Rod Set Position (deg) [rod ange when SPACE was pressed]
    1. Roll Direction [“clockwise”, “counterclockwise”, or “N/A” in static condition]
    1. Roll Velocity (deg/s) [“N/A” in static condition]

## Reproducibility notes

The “Randomisation seed” deterministically sets:

- The dot field layout.
- The sign (+/−) of the initial rod angle on each trial.

Keep seed, appearance parameters, and display geometry constant across sessions for strict reproducibility.

## Performance notes

- The program pre-builds 720 rotated frames (0.5° steps) for smooth disk animation in motion condition (equivalent to 60 fps); launch after setup may take a moment (~1 min).