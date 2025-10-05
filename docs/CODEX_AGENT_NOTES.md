# Notes for Codex Agents (Local Repo)

These reminders are intended for Codex agents working inside the local `picar-x` checkout on macOS.

## Context
- The PiCar-X hardware lives on the Raspberry Pi at `pi@192.168.1.29` (password `picar`).
- The Pi uses a Python virtualenv at `/home/pi/picar_venv`; most scripts run with `sudo /home/pi/picar_venv/bin/python ...`.
- As of 2025-10-05, the Pi’s repo is behind `origin/v2.0`. Several helper files (e.g., `scripts/hourly_chime.py`) were copied manually via `scp`.
- Hourly chime is currently running in the background (`pgrep -f hourly_chime.py`). Stop with `sudo pkill -f hourly_chime.py` if necessary.
- Camera is not detected yet (`rpicam-hello --list-cameras` → “No cameras available!”). Use `sudo raspi-config` and reseat the ribbon before running image demos.

## Typical Commands
```
# local repository tests
PYTHONPYCACHEPREFIX=.pycache python3 -m compileall gpt_examples

# copy files to the Pi
sshpass -p 'picar' scp -o StrictHostKeyChecking=no <local_path> \
  pi@192.168.1.29:/home/pi/picar-x/<remote_path>

# run GPT car in keyboard mode without camera
sshpass -p 'picar' ssh -tt -o StrictHostKeyChecking=no pi@192.168.1.29 \
  "cd /home/pi/picar-x/gpt_examples && sudo /home/pi/picar_venv/bin/python gpt_car.py --keyboard --no-img"

# run Piper voice override
sshpass -p 'picar' ssh -tt -o StrictHostKeyChecking=no pi@192.168.1.29 \
  "cd /home/pi/picar-x/gpt_examples && sudo /home/pi/picar_venv/bin/python gpt_car.py --keyboard --no-img --voice-path voices/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx"

# announce the time on demand (local mac or Pi)
sudo python3 scripts/saytime.py
```

## Watchouts
- Do **not** commit real API keys; `gpt_examples/keys.py` is ignored locally.
- The hourly chime script writes logs to `/home/pi/picar-x/hourly_chime.log` on the Pi. Clean up if running long term.
- Many examples expect root access for audio output. Remind users to run with `sudo` where flagged.
- When testing on macOS without hardware, expect import failures (e.g., `ModuleNotFoundError: robot_hat`). Wrap tests accordingly.

## Useful Docs
- `docs/EXAMPLE_GUIDE.md` – describes every demo script and how to launch each one.
- `docs/NEXT_STEPS.md` – ongoing backlog (camera fix, smoother shutdowns, packaging updates).
- `docs/HOURLY_CHIME.log` (on Pi) – runtime record of the chime script.

Update this file whenever you learn new environment constraints or common troubleshooting steps.
