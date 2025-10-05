# PiCar-X Adventure Guide

*Made for curious kids (around 7 years old) who want to explore and stay safe while playing with PiCar-X.*

## Meet Your PiCar-X
- **Robot Body:** Wheels, motors, lights, and a camera. They let your car drive, turn, and see.
- **Robot Brain:** A Raspberry Pi computer. It remembers your programs and talks to the car.
- **Robot “Hat”:** A special board (Robot HAT) that connects the brain to the motors, sensors, speaker, and more.

## Safety First!
1. **Ask a grown-up for help** with wires, batteries, and chargers.
2. **Keep fingers away from wheels** when the car is on.
3. **Don’t pull the cables**; gently unplug them.
4. **Charge the battery safely** and never leave it plugged in overnight.
5. **Use the car on a flat floor** (no stairs!) so it doesn’t fall.

## Getting Ready
- Check that all wires are plugged in firmly.
- Make sure the battery is full or plug in a safe power supply.
- Gently lift the PiCar-X so the wheels can spin without hitting anything when you test it.
- A helper can turn it on and type commands on the computer.

## Fun Things To Try

| Program | What happens? | How to play |
| --- | --- | --- |
| `example/1.move.py` | The wheels spin forward and the front wheels steer left and right. | Watch from a safe distance while the car is lifted so the wheels can spin freely. |
| `example/2.keyboard_control.py` | You drive the car with the keys `W A S D`, and move the camera with `I J K L`. | Sit with a helper who can type. Drive slowly and avoid pets! |
| `example/3.tts_example.py` | The car honks, plays a song, and says “Hello.” | Press the keys shown on screen to make different sounds. |
| `example/4.avoiding_obstacles.py` | The car drives forward and turns or backs up when it sees something in front of it. | Place a box or toy in front of the car and watch it react. |
| `example/5.minecart_plus.py` | The car follows a dark line on the floor. | Ask a helper to draw a thick black track and let the car follow it. |
| `example/6.cliff_detection.py` | The car stops and backs away when it reaches the edge of a table or a bright line. | Try it near a bright strip or edge (with help so it doesn’t fall). |
| `example/7.display.py` | A special screen shows colors, faces, and QR codes the camera sees. | Use the keyboard to switch modes and watch the display with an adult. |
| `example/8.stare_at_you.py` | The camera looks left, right, up, and down to follow your face. | Smile at the car and see it “stare” at you. |
| `example/9.record_video.py` | Start and stop video recordings from the keyboard. | Make a short movie of your car driving around. |
| `example/10.bull_fight.py` | The car turns toward red objects and chases them. | Wave a red toy and see the car follow it. |
| `example/11.video_car.py` | Control the car from a computer screen, take photos, and see live video. | Ask an adult to start the program, then drive carefully while watching the video feed. |
| `example/12.treasure_hunt.py` | The car tells you a color to find and cheers when it sees it. | Hold up colored cards and try the one it asks for. |
| `example/13.app_control.py` | Drive the car with a phone/tablet app, use line-following, horn, and more. | Pair the SunFounder app (adult help needed) and explore the buttons. |

Each program is explained in `docs/EXAMPLE_GUIDE.md`. Ask your grown-up to help you open it and start the programs safely.

## Parent / Mentor Corner – What Each Program Exercises

| Program | Focused Hardware/Library | Notes |
| --- | --- | --- |
| `example/1.move.py` | `picarx.Picarx` motors & steering servo | Calls `forward()` and `set_dir_servo_angle()` to confirm drivetrain calibration. |
| `example/2.keyboard_control.py` | `readchar`, grayscale, camera servos | Demonstrates keyboard event loop, includes helpers to persist grayscale references in `/opt/picar-x/picar-x.conf`. |
| `example/3.tts_example.py` | `robot_hat.Music`, `robot_hat.TTS` | Exercises audio stack; ensure speaker line (`GPIO20`) is high. |
| `example/4.avoiding_obstacles.py` | Ultrasonic sensor via `Picarx.ultrasonic` | Simple distance thresholds (Safe 40 cm, Danger 20 cm). Adjust constants for different rooms. |
| `example/5.minecart_plus.py` | Grayscale array, line following logic | Uses `get_line_status()`; requires prior calibration (`example/calibration/grayscale_calibration.py`). |
| `example/6.cliff_detection.py` | Grayscale + TTS | Alerts via speech when reflectance drops below cliff threshold. |
| `example/7.display.py` | Vilib Flask server, keyboard controls | Starts camera stream (`Vilib.display`); keys toggle color, face, QR, recording. |
| `example/8.stare_at_you.py` | Face detection, pan/tilt servos | Maps face centroid to servo angles with clamping. |
| `example/9.record_video.py` | Vilib recorder | Manages recording state machine (`record/pause/stop`) writing to `~/Videos/picar-x`. |
| `example/10.bull_fight.py` | Color detection driving loop | Uses `Vilib.color_detect('red')` and servo corrections toward target. |
| `example/11.video_car.py` | Mixed keyboard teleop + photo capture | Streams MJPEG (`Vilib.display(local=True,web=True)`) and writes snapshots to `~/Pictures/picar-x/`. |
| `example/12.treasure_hunt.py` | Color detect + threading + TTS | Randomly selects target colors and announces via `robot_hat.TTS`. |
| `example/13.app_control.py` | SunFounderController app integration | Publishes telemetry and handles joystick/voice toggles, line-following, obstacle avoidance. |
| `example/calibration/` | Grayscale sensor calibration | Writes reference values to `fileDB` entries. |
| `gpt_examples/gpt_car.py` | OpenRouter chat + Piper TTS | Requires mic, speaker, optional camera; fallback to Piper voice when OpenRouter TTS disabled. |
| `scripts/hourly_chime.py` | `robot_hat.TTS`, scheduling | Speaks time hourly (08:00–19:00). |
| `scripts/saytime.py` | `robot_hat.TTS` | Speaks current time on demand; customizable prefix/language. |

For deeper technical context, see `docs/EXAMPLE_GUIDE.md`, `docs/EXAMPLE_GUIDE.md#Other Utilities`, and `docs/NEXT_STEPS.md`.

## Talking to Your Car (with Help)
- Have a supervisor run `gpt_examples/gpt_car.py --keyboard` so you can type messages to the car.
- To let the car listen to your voice, run it without `--keyboard` and talk loudly and clearly.
- Always let an adult handle the microphone and speaker wires. Make sure the speaker is turned on (`sudo pinctrl set 20 op dh`).

## Using Your Imagination
- Build an obstacle course with toys and boxes.
- Pretend the car is delivering tiny packages.
- Draw a track on paper with a thick black line and try the line-following program.
- Turn the car into a friendly pet robot. Give it a name and make it “talk” using the TTS program.

## Keep Learning
- `docs/CODEX_AGENT_NOTES.md` and `docs/CODEX_AGENT_NOTES_PI.md` (for adults) explain how grown-ups can fix things.
- Draw diagrams of your car and label each part.
- Keep a notebook of ideas and what you tried.

Have fun exploring, and always play with care!
