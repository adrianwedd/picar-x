# PiCar-X (Pi) Next Steps for Codex Agents

The Raspberry Pi at `pi@192.168.1.29` hosts the physical robot. Use these notes while debugging or extending the system on-device.

## Current State (2025-10-05)
- Repo aligns with `origin/v2.0` after a hard reset; local changes were cleared and keys restored.
- `/home/pi/picar_venv/bin/python` is the virtualenv used for all robot scripts.
- `gpt_examples/keys.py` already contains the OpenRouter credentials and Piper voice path (`en_US-amy-low`).
- Piper voices located under `gpt_examples/voices/`; saytime/hourly chime scripts live in `scripts/`.
- Hourly chime is running (`sudo pkill -f hourly_chime.py` to stop). Log file: `/home/pi/picar-x/hourly_chime.log`.
- Camera still undetected (`rpicam-hello --list-cameras` → “No cameras available”).

## Recommended Next Steps
1. **Fix Picamera2 detection**
   - Reseat the CSI ribbon cable, ensure camera interface is enabled (`sudo raspi-config → Interface Options → Camera`), reboot, and run `rpicam-hello --list-cameras` until a sensor is listed.
   - Capture a test frame with `rpicam-jpeg -o /tmp/test.jpg` to confirm.

2. **Recover GPT voice agent**
   - If you see `RuntimeError: 'GPIO busy'`, reboot or power-cycle the Robot HAT to release the MCU reset pin (`MCURST`).
   - Relaunch voice mode without camera: `sudo /home/pi/picar_venv/bin/python gpt_examples/gpt_car.py --no-img`.
   - Verify TTS by running `sudo pinctrl set 20 op dh && sudo python3 scripts/saytime.py`.

3. **Inspect running services**
   - Use `pgrep -f gpt_car.py`, `pgrep -f hourly_chime.py`, and `sudo systemctl status autostart.service` (if enabled) to check background processes.

4. **Log review**
   - GPT agent: `/home/pi/picar-x/gpt_examples/gpt_car.log` (if run via nohup).
   - Hourly chime: `/home/pi/picar-x/hourly_chime.log`.
   - Saytime is on-demand; no persistent log.

5. **Cleanup**
   - Remove leftover build artifacts under `/home/pi/picar-x/dist/` or `picarx.egg-info` if they reappear.
   - Delete temporary files (e.g., `/tmp/test.jpg`) after camera testing.

## Quick Commands
```
# Start voice agent in keyboard mode without image capture
cd /home/pi/picar-x/gpt_examples
sudo /home/pi/picar_venv/bin/python gpt_car.py --keyboard --no-img

# Announce current time once
sudo pinctrl set 20 op dh
sudo python3 /home/pi/picar-x/scripts/saytime.py

# Restart hourly chime
cd /home/pi/picar-x
sudo pkill -f hourly_chime.py
sudo nohup /home/pi/picar_venv/bin/python scripts/hourly_chime.py >hourly_chime.log 2>&1 &
```

Update this note when the camera issue is solved or new services are added.
