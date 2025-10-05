# Demo Program Guide

This guide catalogs every script shipped under `example/` and `gpt_examples/`, summarizing what each one does, the hardware or services it relies on, and how to launch it safely on a PiCar-X.

## Quick Reference

| Script | Purpose | Key Requirements |
| --- | --- | --- |
| `example/1.move.py` | Sanity-check motors & steering | Car assembled; run with `sudo`
| `example/2.keyboard_control.py` | Full keyboard teleop (drive + camera servos) | USB keyboard on Pi; `sudo`
| `example/3.tts_example.py` | Exercise Music/TTS playback | Speakers wired, run with `sudo`
| `example/4.avoiding_obstacles.py` | Ultrasonic-based obstacle avoidance | Ultrasonic sensor wired/calibrated
| `example/5.minecart_plus.py` | Line-following demo | Grayscale sensors calibrated
| `example/6.cliff_detection.py` | Cliff detection + spoken alerts | Grayscale sensors + speaker
| `example/7.display.py` | Vision dashboard (color/face/QR) | Camera attached, Vilib running
| `example/8.stare_at_you.py` | Pan/tilt face tracking | Camera + pan/tilt servos
| `example/9.record_video.py` | Keyboard-controlled recording | Camera + storage under `~/Videos`
| `example/10.bull_fight.py` | Charge toward red objects | Camera + servo steering
| `example/11.video_car.py` | Browser-stream teleop + photo capture | Camera, network, keyboard
| `example/12.treasure_hunt.py` | Color treasure hunt minigame | Camera, speaker, keyboard
| `example/13.app_control.py` | SunFounder app remote control | SunFounder mobile app, network
| `example/calibration/*.py` | Sensor calibration helpers | Grayscale board, flat surface
| `example/servo_zeroing.py` | Zero all servos | Car on stand, run with `sudo`
| `gpt_examples/gpt_car.py` | GPT-driven agent with Piper fallback | OpenRouter key, mic, speaker, camera
| `gpt_examples/preset_actions.py` | Preview canned actions/sounds | Motors/servos connected
| `scripts/hourly_chime.py` | Hourly time announcement (08:00–19:00) | Speaker, run with `sudo`
| `scripts/saytime.py` | Speak the current time on demand | Speaker, run with `sudo`
| `gpt_examples/friendly_logger.py` | Colorful kid-friendly logging helper | Import and call `friendly_log(...)` in demos

Scripts not listed in the table are either modules imported elsewhere or legacy helpers.

## Standard Examples (`example/`)

### 1.move.py – Motion Smoke Test
- **What it does:** Instantiates `Picarx`, spins the rear motors forward briefly, then sweeps the steering servo from full left to full right and back. Use it after mechanical reassembly to confirm nothing binds.
- **Run:** `sudo python3 example/1.move.py`
- **Notes:** Runs in a `try/finally` block but does not explicitly stop motors if interrupted extremely early; keep wheels off the ground.

### 2.keyboard_control.py – Teleoperation Playground
- **What it does:** Provides WASD drive control and IJKL camera pan/tilt via keyboard, plus routines for calibrating the grayscale module in software.
- **Run:** `sudo python3 example/2.keyboard_control.py`
- **Controls:**
  - `w/a/s/d` drive, `i/k` tilt camera, `j/l` pan camera, `ctrl+c` twice to exit.
- **Prereqs:** USB keyboard (or SSH session forwarding keystrokes), speaker optional for printed prompts.
- **Extras:** Contains helper methods for storing grayscale baselines to `/opt/picar-x/picar-x.conf`.

### 3.tts_example.py – Audio Systems Check
- **What it does:** Demonstrates `Music` (background music + horn) and `TTS` playback. Keyboard shortcuts trigger WAV/MP3 playback and synthesize the phrase “Hello”.
- **Run:** `sudo python3 example/3.tts_example.py`
- **Controls:**
  - `space` horn, `c` horn (threaded), `t` speak “Hello”, `q` toggle BGM.
- **Prereqs:** Speakers plugged into Robot HAT. Script warns if not launched as root.

### 4.avoiding_obstacles.py – Ultrasonic Avoidance
- **What it does:** Polls `px.ultrasonic.read()` continuously and adjusts direction/speed based on distance thresholds (40 cm safe, 20–40 cm turn, <20 cm reverse).
- **Run:** `sudo python3 example/4.avoiding_obstacles.py`
- **Prereqs:** Ultrasonic module connected; ensure the field around the car is clear.

### 5.minecart_plus.py – Line Following
- **What it does:** Uses the three-channel grayscale module to follow a dark line. When the sensor loses the line, it backs up and re-acquires based on the previous steering direction.
- **Run:** `sudo python3 example/5.minecart_plus.py`
- **Prereqs:** Calibrate the grayscale sensors first (`example/calibration/grayscale_calibration.py`) or set `px.set_line_reference([...])` manually.
- **Tips:** Adjust `px_power` and `offset` to tune response on your surface.

### 6.cliff_detection.py – Drop-Off Guard
- **What it does:** Reuses the grayscale module but treats low reflectance as a “cliff” trigger. When detected, the robot halts, speaks an alert, and backs away.
- **Run:** `sudo python3 example/6.cliff_detection.py`
- **Prereqs:** Speaker for TTS output; calibrate cliff references similar to the line follower.

### 7.display.py – Vision Dashboard
- **What it does:** Starts Vilib, opens a local display window, and maps keyboard hotkeys to color detection, face detection, QR scanning, manual capture, and recording.
- **Run:** `sudo python3 example/7.display.py`
- **Controls:** Keys `1`–`6` for color detection (red→purple), `q` snapshot, `v`/`z` record, `f` face detect, `h` human detection, etc. (see in-script manual).
- **Prereqs:** Camera connected; Vilib’s Flask server uses port `9000` by default.

### 8.stare_at_you.py – Face Tracking
- **What it does:** Uses Vilib face detection to keep a detected face roughly centered by adjusting pan/tilt angles.
- **Run:** `sudo python3 example/8.stare_at_you.py`
- **Prereqs:** Camera plus pan/tilt servos calibrated. Contains `clamp_number` utility to bound servo angles.

### 9.record_video.py – Keyboard Recorder
- **What it does:** Toggles Vilib recording to the user’s `~/Videos/picar-x/` directory; shows time stamps and status in the terminal.
- **Run:** `sudo python3 example/9.record_video.py`
- **Controls:** `q` start/pause resume, `e` stop/save, `ctrl+c` quit.
- **Prereqs:** Camera; ensure target directory exists and has enough disk space.

### 10.bull_fight.py – Color-Chasing Bot
- **What it does:** Tracks the centroid of a chosen color (default red) and turns toward it while adjusting speed proportionally. The car “charges” detected targets.
- **Run:** `sudo python3 example/10.bull_fight.py`
- **Prereqs:** Camera installed; color detection thresholds tuned for environment.

### 11.video_car.py – Web Teleop with Snapshots
- **What it does:** Starts Vilib streaming (local window + MJPEG web stream) and maps keyboard controls for driving, speed adjustments, and photo capture into `~/Pictures/picar-x/`.
- **Run:** `sudo python3 example/11.video_car.py`
- **Controls:** `o/p` speed up/down, `w/a/s/d` motion, `f` stop, `t` photo, `ctrl+c` exit.
- **Notes:** Resets the MCU before starting; prints current drive status continuously.

### 12.treasure_hunt.py – Color Hunt Minigame
- **What it does:** Randomly selects a color target, announces it via TTS, and monitors detection. When the target is found (width threshold >100), congratulates and picks a new color.
- **Run:** `sudo python3 example/12.treasure_hunt.py`
- **Controls:** WASD drive, `space` repeat target, `ctrl+c` exit.
- **Prereqs:** Camera, speaker for TTS, optional music.

### 13.app_control.py – SunFounder App Integration
- **What it does:** Hooks into the SunFounder mobile app via `SunFounderController`, exposes telemetry (distance, grayscale, video URL) and responds to virtual joystick, speech commands, horn button, line-tracking toggle, obstacle avoidance toggle, and image recognition toggles.
- **Run:** `sudo python3 example/13.app_control.py`
- **Prereqs:** SunFounder Controller app configured to discover the PiCar-X on the network; camera and sensors connected; speaker for horn/audio feedback.
- **Highlights:** Combines multiple behaviours: joystick drive, servo control, color/face/object detection, line following, obstacle avoidance.

### Calibration Tools
- **`example/calibration/grayscale_calibration.py`** – Guides you through sampling white/black surfaces, then writes calibrated values to the config file.
- **`example/calibration/calibration.py`** – General helper invoked by other scripts to persist calibration values.
- **`example/servo_zeroing.py`** – Resets all 12 servo channels to zero (requires `sudo`). Use when servos drift or after reassembly.

## GPT Examples (`gpt_examples/`)

### gpt_car.py – Chat-Driven Agent
- **Purpose:** End-to-end assistant that listens via microphone or keyboard, optionally uploads camera frames, and responds with actions, speech, and sound effects.
- **Key flags:**
  - `--keyboard` / default voice input
  - `--no-img` to skip camera capture (useful if Picamera2 isn’t available)
  - `--voice-path PATH` to override Piper voice per run
- **Configuration:** Fill in `OPENROUTER_*` values in `gpt_examples/keys.py`. Leave `OPENROUTER_TTS_MODEL` empty to use Piper/espeak fallback. Point `PIPER_VOICE_PATH` at any downloaded `.onnx` voice.
- **Dependencies:** OpenRouter API access, `piper-tts`, `SpeechRecognition`, SoX, Vilib (for camera capture), microphone, speaker. Run with `sudo` to avoid audio permission issues.

### openrouter_helper.py
- Wrapper around OpenRouter REST endpoints providing chat, vision, STT, and TTS helpers. Used exclusively by `gpt_car.py`.

### preset_actions.py
- Defines motion and sound routines (e.g., `shake_head`, `celebrate`, `honking`). Run `python3 gpt_examples/preset_actions.py` to preview actions when your car is safely lifted.

### utils.py
- Shared utility functions for colored terminal output, SoX gain adjustments, and sound playback.

### scripts/hourly_chime.py
- Announces the current time on the hour between 08:00 and 19:00 using the Robot HAT speaker.
- Run with `sudo python3 scripts/hourly_chime.py`; keep the Pi powered and the speaker enabled (for some hats, `pinctrl set 20 op dh`).
- Modify `START_HOUR`/`END_HOUR` in the script to change the schedule.

### scripts/saytime.py
- Announces the current time once. Supports optional `--lang` and `--prefix` arguments to customize voice and phrasing.
- Run with `sudo python3 scripts/saytime.py` whenever you want a spoken clock update.

### gpt_examples/friendly_logger.py
- Provides the `friendly_log` helper used by `example/2.keyboard_control.py` to print emoji-rich, color-coded messages.
- Import with `from gpt_examples.friendly_logger import friendly_log` and call `friendly_log("move", "Zoom!", color="green")` to add playful logging to new demos.

## Operational Checklist

1. **Update firmware & packages:** Ensure `sudo apt update && sudo apt upgrade` has been run recently, and install `piper-tts`, `SpeechRecognition`, `libcamera` tools as shown above.
2. **Calibrate sensors:** Before line/cliff demos, execute `sudo python3 example/calibration/grayscale_calibration.py` on the driving surface.
3. **Check audio:** Run `sudo python3 example/3.tts_example.py` to confirm the speaker works before using GPT or treasure-hunt scripts.
4. **Verify camera:** Use `rpicam-hello --list-cameras` (after installing `rpicam-apps`) to ensure Picamera2 detects your module.
5. **Secure the car:** Place the vehicle on a stand or hold it firmly when testing scripts that move motors without keyboard interruption.

## Documentation Maintenance

- The commands above assume you are inside the repository root (`/home/pi/picar-x/`).
- Update this guide when new demos are added or behaviour changes significantly.
- If you customize scripts (e.g., different sensor pins), note the changes alongside the relevant section for future contributors.
