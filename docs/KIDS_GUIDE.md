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
- `example/1.move.py` – See the wheels turn.
- `example/2.keyboard_control.py` – Drive with the keys `W A S D`.
- `example/3.tts_example.py` – Make the car talk and play music.
- `example/4.avoiding_obstacles.py` – Watch it stop before bumping into things.
- `gpt_examples/gpt_car.py --keyboard` – Have a chatty assistant control the car! (Use with an adult because it needs an internet connection.)

Each program is explained in `docs/EXAMPLE_GUIDE.md`. Ask your grown-up to help you open it.

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
