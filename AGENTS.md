# Repository Guidelines

## Quick Links & References
- `docs/EXAMPLE_GUIDE.md` – launch instructions for every demo script.
- `docs/NEXT_STEPS.md` – engineering backlog (camera fix, testing hooks, packaging).
- `docs/CODEX_AGENT_NOTES.md` – tips for working in the macOS repo clone.
- `docs/CODEX_AGENT_NOTES_PI.md` – status and commands for the live Pi at `pi@192.168.1.29`.
- `scripts/` – utility helpers (`hourly_chime.py`, `saytime.py`).

## Project Structure & Module Organization
The core Python package lives in `picarx/`, with `picarx.py` exposing motor, servo, ultrasonic, and grayscale control plus `/opt/picar-x/picar-x.conf` calibration helpers. Example-driving scripts are grouped under `example/`; the `calibration/` subfolder and `servo_zeroing.py` are the quickest way to align hardware before testing new behaviors (see `docs/EXAMPLE_GUIDE.md` for per-script details). Conversational and GPT-enabled workflows sit in `gpt_examples/` alongside `tutorial_*.png` walkthroughs and helper utilities. Audio assets for reactions and prompts are stored in `musics/` and `sounds/`, while provisioning helpers such as `autostart.service` and `i2samp.sh` support deployment on Raspberry Pi OS.

## Build, Test, and Development Commands
Use an isolated env when iterating:
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```
Installing on-device still supports `sudo python3 setup.py install` per `README.md`. Run an interactive demo with `sudo python3 example/2.keyboard_control.py`, and explore the GPT integration using `sudo python3 gpt_examples/gpt_car.py --keyboard`. Keep firmware responsive by restarting the MCU after flashing with `robot-hat enable_speaker` or `utils.reset_mcu()` inside Python.

### On the Pi (robot)
- SSH with `sshpass -p 'picar' ssh pi@192.168.1.29`.
- Repository root: `/home/pi/picar-x`; virtualenv: `/home/pi/picar_venv/`.
- Sync to latest: `git fetch origin && git reset --hard origin/v2.0` (back up `gpt_examples/keys.py` first—it's ignored locally).
- Launch GPT keyboard mode: `cd gpt_examples && sudo /home/pi/picar_venv/bin/python gpt_car.py --keyboard --no-img`.
- Enable speaker if muted: `sudo pinctrl set 20 op dh`.
- Quick utilities: `sudo python3 scripts/saytime.py` (speak once), `sudo pkill -f hourly_chime.py` / restart via the command in `docs/CODEX_AGENT_NOTES_PI.md`.

## Coding Style & Naming Conventions
Follow PEP 8 defaults: four-space indents, lowercase_with_underscores for functions, and CapWords classes. Hardware pin constants should stay uppercase (see `Picarx.CONFIG`). Prefer descriptive docstrings over inline comments, and keep calibration defaults centralized in `Picarx` class attributes. Run `python3 -m compileall picarx` or a linter such as `ruff` before sending a pull request.

## Testing Guidelines
Adopt `pytest` for new coverage. Place files under `tests/` mirroring the module layout (e.g., `tests/test_picarx.py`) and name fixtures with `pytest`'s snake_case convention. Aim for ≥80% statement coverage on motion and sensor logic; spot-check hardware effects with dry-run mocks before powering motors. Execute suites locally via `pytest -q` and capture logs from any physical runs.

## Commit & Pull Request Guidelines
Recent history favors short, imperative subjects like `add tts voice instructions`; keep them under 50 characters and reference issues with `(#123)` when relevant. Bundle calibration data or media changes in separate commits to simplify review. Pull requests should explain the hardware state used for validation, list command output (tests, demos), and attach screenshots or terminal snippets for UI/audio updates. Mention any new dependencies or configuration files so deployment scripts can be updated promptly.

`gpt_examples/keys.py` is ignored—never commit real API keys. When testing on the Pi, copy the template and fill in credentials locally.

## Hardware & Configuration Tips
Back up `/opt/picar-x/picar-x.conf` before altering calibration routines, and reset via `fileDB` helpers when switching vehicles. Confirm that `robot_hat`, `vilib`, and other upstream libraries match the versions documented in `README.md`, and document any GPIO remaps needed for custom chassis. If the camera stops responding, reseat the CSI ribbon, enable the interface in `sudo raspi-config`, and verify with `rpicam-hello --list-cameras` before running vision demos.
