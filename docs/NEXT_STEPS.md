# PiCar-X Next Steps

This checklist captures outstanding work needed to bring the PiCar-X demo stack to a production-ready state.

## 1. Restore Camera Functionality
- **Goal:** Picamera2 must detect the camera so `Vilib` and the GPT vision path can start without `--no-img`.
- **Actions:**
  - Power down the Pi, reseat the CSI ribbon (contacts toward HDMI ports) and ensure the locking tabs are secure.
  - Boot and run `rpicam-hello --list-cameras`. It should list at least one sensor; if not, enable the interface via `sudo raspi-config → Interface Options → Camera`, reboot, and re-test.
  - Once detection succeeds, capture a test image (`rpicam-jpeg -o /tmp/test.jpg`) to verify streaming works.
  - Re-run `sudo /home/pi/picar_venv/bin/python gpt_car.py` without `--no-img` to validate Vilib integration.

## 2. Smooth Shutdown for gpt_car Threads
- **Observation:** Keyboard-mode runs exit with `Exception in thread Thread-3 (action_handler)` when stdin closes.
- **Plan:**
  - Add a shared shutdown flag that breaks the action and speak threads when `main()` exits.
  - Ensure `finally` block stops Vilib, resets the car, and joins worker threads.
  - Re-test both keyboard and voice modes for clean termination.

## 3. Broaden Voice Library (Optional)
- **Goal:** Offer multiple Piper voices out of the box.
- **Actions:**
  - Pull additional `en_*` voices into `gpt_examples/voices/` (e.g., `en_GB/alan`, `en_US/ljspeech`).
  - Update `docs/EXAMPLE_GUIDE.md` and `gpt_examples/README.md` with new aliases and recommendations.
  - Provide a convenience script for voice downloads (e.g., `scripts/install_piper_voice.py`).

## 4. Hardware Validation Suite
- **Goal:** Create a single entry point to verify sensors/actuators (motors, servos, ultrasonic, grayscale, speaker, camera).
- **Actions:**
  - Compose a `docs/VALIDATION_CHECKLIST.md` summarizing which example to run for each subsystem.
  - Consider a simple CLI harness (`python3 tools/diagnostics.py`) that runs smoke tests sequentially.

## 5. Automated Testing Hooks
- **Goal:** Improve confidence before merging changes.
- **Actions:**
  - Introduce lightweight unit tests for helper modules (`gpt_examples/openrouter_helper.py`, `gpt_examples/utils.py`) using mock requests.
  - Add tox or nox recipes for linting (`ruff`, `black`) and formatting.
  - Document the workflow in `AGENTS.md` or a new `CONTRIBUTING.md` section.

## 6. Deployment & Packaging
- **Goal:** Simplify setup for new robots.
- **Actions:**
  - Bundle requirements into `requirements.txt` (host) and `requirements-pi.txt` (Pi-specific).
  - Provide an install script that provisions the venv, installs dependencies, downloads Piper voices, and copies example configs.
  - Evaluate publishing `picarx` to PyPI or GitHub Releases for easier upgrades.

## 7. Optional Enhancements
- Controller integration improvements (touch gestures → actions).
- Record/replay trajectories for classroom demos.
- Voice-only fallback script for low-resource modes (Vilib optional).

## Status Tracking
- Use this document as a living backlog; append checkboxes or dates as tasks complete.
- Reference it in pull requests when addressing items.

