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
- Ask a helper to turn the car on and log in to the computer.

### Step-by-Step: Running a Program Together
1. **Open a terminal** (black window with text) on the Pi or on a computer connected with SSH.
2. **Go to the robot’s folder:**
   ```bash
   cd /home/pi/picar-x
   ```
3. **Choose a demo** from the table below.
4. **Type `sudo /home/pi/picar_venv/bin/python <path/to/demo.py>`** and press Enter. (This Python has all the robot tools pre-installed.)
5. **Watch what happens!** Keep hands away from the wheels.
6. **Stop anytime** with `Ctrl` + `C` (press the keys at the same time). Press twice if the program keeps running.

> Grown-ups: running with `sudo` gives the script permission to control hardware (motors, speaker, sensors). Stay nearby while kids experiment.

## Fun Things To Try

| Program | What happens? | How to play |
| --- | --- | --- |
| `example/1.move.py` | The wheels spin forward and the front wheels steer left and right. | Watch from a safe distance while the car is lifted so the wheels can spin freely. |
| `example/2.keyboard_control.py` | You drive the car with the keys `W A S D`, and move the camera with `I J K L`. | Needs a real keyboard plugged into the Pi or an SSH session opened with `ssh -tt`. Drive slowly and avoid pets! |
| `example/3.tts_example.py` | The car honks, plays a song, and says “Hello.” | Needs a real keyboard (`ssh -tt` or HDMI). Press the keys shown on screen to make different sounds. |
| `example/4.avoiding_obstacles.py` | The car drives forward and turns or backs up when it sees something in front of it. | Place a box or toy in front of the car and watch it react. |
| `example/5.minecart_plus.py` | The car follows a dark line on the floor. | Ask a helper to draw a thick black track and let the car follow it. |
| `example/6.cliff_detection.py` | The car stops and backs away when it reaches the edge of a table or a bright line. | Try it near a bright strip or edge (with help so it doesn’t fall). |
| `example/7.display.py` | A special screen shows colors, faces, and QR codes the camera sees. | Open a browser to `http://<pi-address>:9000/mjpg` or plug in an HDMI display to see the video.
| `example/8.stare_at_you.py` | The camera looks left, right, up, and down to follow your face. | Smile at the car and see it “stare” at you. |
| `example/9.record_video.py` | Start and stop video recordings from the keyboard. | Needs a real keyboard (`ssh -tt` or HDMI). Make a short movie of your car driving around. |
| `example/10.bull_fight.py` | The car turns toward red objects and chases them. | Watch the live video at `http://<pi-address>:9000/mjpg` (or HDMI) to see what the camera sees. |
| `example/11.video_car.py` | Control the car from a computer screen, take photos, and see live video. | Visit `http://<pi-address>:9000/mjpg` in a browser for the stream; then use the keyboard to drive. |
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
| `gpt_examples/gpt_car.py` | OpenRouter chat + Piper TTS | Requires mic, speaker, optional camera; needs `OPENROUTER_API_KEY` set in `gpt_examples/keys.py`. |
| `scripts/hourly_chime.py` | `robot_hat.TTS`, scheduling | Speaks time hourly (08:00–19:00). |
| `scripts/saytime.py` | `robot_hat.TTS` | Speaks current time on demand; customizable prefix/language. |

For deeper technical context, see `docs/EXAMPLE_GUIDE.md`, `docs/EXAMPLE_GUIDE.md#Other Utilities`, and `docs/NEXT_STEPS.md`.

## Talking to Your Car (with Help)
- Have a supervisor run `gpt_examples/gpt_car.py --keyboard` so you can type messages to the car. (Make sure your helper puts the OpenRouter API key into `gpt_examples/keys.py` first.)
- To let the car listen to your voice, run it without `--keyboard` and talk loudly and clearly.
- Always let an adult handle the microphone and speaker wires. Make sure the speaker is turned on (`sudo pinctrl set 20 op dh`).
- If the car says it cannot hear you, stop the program (`Ctrl` + `C`), check the microphone plug, and try again.

## Using Your Imagination
- Build an obstacle course with toys and boxes.
- Pretend the car is delivering tiny packages.
- Draw a track on paper with a thick black line and try the line-following program.
- Turn the car into a friendly pet robot. Give it a name and make it “talk” using the TTS program.
- Ask a Codex helper (a friendly coding agent) to write a new mini-game! Try saying, “Can you make the car dance with a new program?” and run the script together with an adult.

## Make New Tricks with Codex (Kid Version)
1. **Grab a grown-up.** Codex needs an adult partner to type and keep things safe.
2. **Explain your idea clearly.** Example: “Codex, please create a program that makes PiCar-X spin in a circle and flash its lights.”
3. **Let Codex write the code.** The helper will create a new Python file (maybe inside the `example/` folder).
4. **Run it together.** In the terminal, type:
   ```bash
   cd /home/pi/picar-x
   sudo /home/pi/picar_venv/bin/python example/my_new_trick.py
   ```
5. **Test, tweak, repeat!** If the car moves too fast or slow, ask Codex to adjust the numbers.

### Kid-Friendly Tech Tips
- Programs that start with `sudo python3` usually talk to motors or speakers.
- If the car says `ModuleNotFoundError`, it means a library is missing—ask Codex or an adult to install it.
- To stop a script quickly, press `Ctrl` + `C` twice.
- Save new ideas in a notebook so Codex can help you build them later.
- If you use SSH from another computer, ask your helper to connect with `ssh -tt` so programs that need a keyboard work properly.

## If Something Goes Wrong
- **Car won’t move?** Check the battery and make sure the wheels aren’t touching the ground while testing.
- **Car is too fast?** Ask Codex to lower the speed number in the code (for example, change `forward(50)` to `forward(20)`).
- **No sound?** Run `sudo pinctrl set 20 op dh` and try the `saytime` program again.
- **Camera not working?** Ask an adult to gently press the camera ribbon cable back in place and reboot the Pi.
- **Unsure what a part does?** Open `docs/EXAMPLE_GUIDE.md` for more explanations or ask Codex for help.

## Keep Learning
- `docs/CODEX_AGENT_NOTES.md` and `docs/CODEX_AGENT_NOTES_PI.md` (for adults) explain how grown-ups can fix things.
- Draw diagrams of your car and label each part.
- Keep a notebook of ideas and what you tried.

Have fun exploring, and always play with care!
