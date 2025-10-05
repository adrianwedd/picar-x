from openrouter_helper import OpenRouterHelper
from keys import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_REFERER,
    OPENROUTER_SITE_TITLE,
    OPENROUTER_STT_MODEL,
    OPENROUTER_SYSTEM_PROMPT,
    OPENROUTER_TTS_MODEL,
    PIPER_LENGTH_SCALE,
    PIPER_SPEAKER_ID,
    PIPER_VOICE_PATH,
)
from preset_actions import *
from utils import *

import readline # optimize keyboard input, only need to import

import speech_recognition as sr

from picarx import Picarx
from robot_hat import Music, Pin

import time
import threading
import random

import os
import sys
import subprocess
import shutil

os.popen("pinctrl set 20 op dh") # enable robot_hat speake switch
current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path) # change working directory

input_mode = None
with_img = True
args = sys.argv[1:]

if '--help' in args or '-h' in args:
    print("Usage: python gpt_car.py [--keyboard] [--no-img] [--voice-path PATH]")
    sys.exit(0)

if '--keyboard' in args:
    input_mode = 'keyboard'
else:
    input_mode = 'voice'

if '--no-img' in args:
    with_img = False
else:
    with_img = True

cli_voice_path = None
if '--voice-path' in args:
    idx = args.index('--voice-path')
    try:
        cli_voice_path = args[idx + 1]
    except IndexError:
        raise ValueError('--voice-path requires a model path argument')

# openrouter assistant init
# =================================================================
openrouter_helper = OpenRouterHelper(
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    'picarx',
    system_prompt=OPENROUTER_SYSTEM_PROMPT,
    referer=OPENROUTER_REFERER or None,
    site_title=OPENROUTER_SITE_TITLE or None,
    stt_model=OPENROUTER_STT_MODEL or None,
    tts_model=OPENROUTER_TTS_MODEL if OPENROUTER_TTS_MODEL != "" else "",
)

LANGUAGE = []
# LANGUAGE = ['zh', 'en'] # config stt language code, https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes

# VOLUME_DB = 5
VOLUME_DB = 3

# select tts voice role, counld be "alloy, echo, fable, onyx, nova, and shimmer"
# https://platform.openai.com/docs/guides/text-to-speech/supported-languages
TTS_VOICE = 'echo'

# voice instructions for vibe
# https://www.openai.fm/
VOICE_INSTRUCTIONS = ""

SOUND_EFFECT_ACTIONS = ["honking", "start engine"]

# local tts helpers
# =================================================================
REMOTE_TTS_VOICES = {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}

_piper_command = os.environ.get("PIPER_COMMAND", "piper")
if not os.path.isabs(_piper_command):
    _piper_command = shutil.which(_piper_command) or _piper_command
if not os.path.isabs(_piper_command):
    candidate = os.path.join(os.path.dirname(sys.executable), os.path.basename(_piper_command))
    if os.path.exists(candidate):
        _piper_command = candidate

resolved_piper_voice = cli_voice_path.strip() if cli_voice_path else PIPER_VOICE_PATH.strip()
if resolved_piper_voice and not os.path.isabs(resolved_piper_voice):
    resolved_piper_voice = os.path.join(current_path, resolved_piper_voice)

try:
    resolved_piper_speaker = int(PIPER_SPEAKER_ID) if PIPER_SPEAKER_ID != "" else None
except ValueError:
    resolved_piper_speaker = PIPER_SPEAKER_ID or None

try:
    resolved_piper_length_scale = float(PIPER_LENGTH_SCALE) if PIPER_LENGTH_SCALE != "" else None
except ValueError:
    resolved_piper_length_scale = None


def _normalise_local_voice(voice: str) -> str:
    if not voice:
        return "en"
    if voice.lower() in REMOTE_TTS_VOICES:
        return "en"
    return voice


def _ensure_output_directory(path: str) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def synthesize_with_piper(
    text: str,
    output_file: str,
    model_path: str,
    speaker: str | int | None = None,
    length_scale: float | None = None,
) -> bool:
    if not model_path:
        return False

    candidates = [model_path]
    if not os.path.isabs(model_path):
        candidates.insert(0, os.path.join(current_path, model_path))

    resolved_model = None
    for path in candidates:
        if os.path.exists(path):
            resolved_model = path
            break

    if resolved_model is None:
        print(f"tts err: piper voice not found ({model_path})")
        return False

    config_path = resolved_model + ".json"
    if not os.path.exists(config_path) and resolved_model.endswith(".onnx"):
        alt_config = resolved_model + ".json"
        alt_guess = resolved_model.replace(".onnx", ".onnx.json")
        config_path = alt_guess if os.path.exists(alt_guess) else config_path

    cmd = [_piper_command, "--model", resolved_model, "--output_file", output_file]
    if os.path.exists(config_path):
        cmd.extend(["--config", config_path])
    if speaker is not None:
        cmd.extend(["--speaker", str(speaker)])
    if length_scale is not None:
        cmd.extend(["--length_scale", str(length_scale)])

    try:
        _ensure_output_directory(output_file)
        subprocess.run(cmd, input=text.encode("utf-8"), check=True)
        return True
    except FileNotFoundError:
        print("tts err: piper command not found")
        return False
    except subprocess.CalledProcessError as exc:
        print(f"tts err: {exc}")
        return False


def synthesize_with_espeak(text: str, output_file: str, voice: str = "en") -> bool:
    try:
        _ensure_output_directory(output_file)
        voice_arg = _normalise_local_voice(voice)
        cmd = ["espeak", "-w", output_file]
        if voice_arg:
            cmd.extend(["-v", voice_arg])
        cmd.append(text)

        subprocess.run(cmd, check=True)
        return True
    except FileNotFoundError:
        print("tts err: espeak command not found")
        return False
    except subprocess.CalledProcessError as exc:
        print(f"tts err: {exc}")
        return False

# car init 
# =================================================================
try:
    my_car = Picarx()
    time.sleep(1)
except Exception as e:
    raise RuntimeError(e)

music = Music()

led = Pin('LED')

DEFAULT_HEAD_PAN = 0
DEFAULT_HEAD_TILT = 20

# Vilib start
# =================================================================
if with_img:
    from vilib import Vilib
    import cv2

    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.show_fps()
    Vilib.display(local=False,web=True)

    while True:
        if Vilib.flask_start:
            break
        time.sleep(0.01)

    time.sleep(.5)
    print('\n')

# speech_recognition init
# =================================================================
'''
self.energy_threshold = 300  # minimum audio energy to consider for recording
self.dynamic_energy_threshold = True
self.dynamic_energy_adjustment_damping = 0.15
self.dynamic_energy_ratio = 1.5
self.pause_threshold = 0.8  # seconds of non-speaking audio before a phrase is considered complete
self.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout

self.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
self.non_speaking_duration = 0.5  # seconds of non-speaking audio to keep on both sides of the recording

'''
recognizer = sr.Recognizer()
recognizer.dynamic_energy_adjustment_damping = 0.16
recognizer.dynamic_energy_ratio = 1.6

# speak_hanlder
# =================================================================
speech_loaded = False
speech_lock = threading.Lock()
tts_file = None

def speak_hanlder():
    global speech_loaded, tts_file
    while True:
        with speech_lock:
            _isloaded = speech_loaded
        if _isloaded:
            # gray_print('speak start')
            speak_block(music, tts_file)
            # gray_print('speak done')
            with speech_lock:
                speech_loaded = False
        time.sleep(0.05)

speak_thread = threading.Thread(target=speak_hanlder)
speak_thread.daemon = True


# actions thread
# =================================================================
action_status = 'standby' # 'standby', 'think', 'actions', 'actions_done'
led_status = 'standby' # 'standby', 'think' or 'actions', 'actions_done'
last_action_status = 'standby'
last_led_status = 'standby'

LED_DOUBLE_BLINK_INTERVAL = 0.8 # seconds
LED_BLINK_INTERVAL = 0.1 # seconds

actions_to_be_done = []
action_lock = threading.Lock()

def action_handler():
    global action_status, actions_to_be_done, led_status, last_action_status, last_led_status

    # standby_actions = ['waiting', 'feet_left_right']
    # standby_weights = [1, 0.3]

    action_interval = 5 # seconds
    last_action_time = time.time()
    last_led_time = time.time()

    while True:
        with action_lock:
            _state = action_status

        # led
        # ------------------------------
        led_status = _state

        if led_status != last_led_status:
            last_led_time = 0
            last_led_status = led_status

        if led_status == 'standby':
            if time.time() - last_led_time > LED_DOUBLE_BLINK_INTERVAL:
                led.off()
                led.on()
                sleep(.1)
                led.off()
                sleep(.1)
                led.on()
                sleep(.1)
                led.off()
                last_led_time = time.time()
        elif led_status == 'think':
            if time.time() - last_led_time > LED_BLINK_INTERVAL:
                led.off()
                sleep(LED_BLINK_INTERVAL)
                led.on()
                sleep(LED_BLINK_INTERVAL)
                last_led_time = time.time()
        elif led_status == 'actions':
                led.on() 

        # actions
        # ------------------------------
        if _state == 'standby':
            last_action_status = 'standby'
            if time.time() - last_action_time > action_interval:
                # TODO: standby actions
                last_action_time = time.time()
                action_interval = random.randint(2, 6)
        elif _state == 'think':
            if last_action_status != 'think':
                last_action_status = 'think'
                # think(my_car)
                keep_think(my_car)
        elif _state == 'actions':
            last_action_status = 'actions'
            with action_lock:
                _actions = actions_to_be_done
            for _action in _actions:
                try:
                    actions_dict[_action](my_car)
                except Exception as e:
                    print(f'action error: {e}')
                time.sleep(0.5)

            with action_lock:
                action_status = 'actions_done'
            last_action_time = time.time()

        time.sleep(0.01)

action_thread = threading.Thread(target=action_handler)
action_thread.daemon = True


# main
# =================================================================
def main():
    global current_feeling, last_feeling
    global speech_loaded
    global action_status, actions_to_be_done
    global tts_file

    my_car.reset()
    my_car.set_cam_tilt_angle(DEFAULT_HEAD_TILT)

    speak_thread.start()
    action_thread.start()

    while True:
        if input_mode == 'voice':
            my_car.set_cam_pan_angle(DEFAULT_HEAD_PAN)
            my_car.set_cam_tilt_angle(DEFAULT_HEAD_TILT)

            # listen
            # ----------------------------------------------------------------
            gray_print("listening ...")

            with action_lock:
                action_status = 'standby'

            _stderr_back = redirect_error_2_null() # ignore error print to ignore ALSA errors
            # If the chunk_size is set too small (default_size=1024), it may cause the program to freeze
            with sr.Microphone(chunk_size=8192) as source:
                cancel_redirect_error(_stderr_back) # restore error print
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            # stt
            # ----------------------------------------------------------------
            gray_print('stt ...')
            st = time.time()
            _result = openrouter_helper.stt(audio, language=LANGUAGE)
            gray_print(f"stt takes: {time.time() - st:.3f} s")

            if _result == False or _result == "":
                print() # new line
                continue

        elif input_mode == 'keyboard':
            my_car.set_cam_tilt_angle(DEFAULT_HEAD_TILT)

            with action_lock:
                action_status = 'standby'

            _result = input(f'\033[1;30m{"intput: "}\033[0m').encode(sys.stdin.encoding).decode('utf-8')

            if _result == False or _result == "":
                print() # new line
                continue

        else:
            raise ValueError("Invalid input mode")

        # chat-gpt
        # ---------------------------------------------------------------- 
        gray_print(f'thinking ...')
        response = {}
        st = time.time()

        with action_lock:
            action_status = 'think'

        if with_img:
            img_path = './img_imput.jpg'
            cv2.imwrite(img_path, Vilib.img)
            response = openrouter_helper.dialogue_with_img(_result, img_path)
        else:
            response = openrouter_helper.dialogue(_result)

        gray_print(f'chat takes: {time.time() - st:.3f} s')

        # actions & TTS
        # ----------------------------------------------------------------
        _sound_actions = []
        actions = []
        answer = ''
        try:
            if isinstance(response, dict):
                raw_actions = response.get('actions', []) or []
                raw_answer = response.get('answer', '')
                answer = raw_answer if isinstance(raw_answer, str) else str(raw_answer)

                extra_speak_segments = []

                for item in raw_actions:
                    action_name = None
                    if isinstance(item, str):
                        action_name = item
                    elif isinstance(item, dict):
                        action_type = item.get('type')
                        if action_type == 'speak':
                            speak_text = item.get('text')
                            if speak_text:
                                extra_speak_segments.append(str(speak_text))
                            continue
                        elif isinstance(action_type, str):
                            action_name = action_type
                        else:
                            gray_print(f"skip unsupported action payload: {item}")
                            continue
                    else:
                        gray_print(f"skip unsupported action: {item}")
                        continue

                    if not action_name:
                        continue

                    if action_name in SOUND_EFFECT_ACTIONS:
                        _sound_actions.append(action_name)
                    elif action_name in actions_dict:
                        actions.append(action_name)
                    else:
                        gray_print(f"unknown action '{action_name}' ignored")

                if extra_speak_segments:
                    extra_text = " ".join(extra_speak_segments).strip()
                    if extra_text:
                        answer = f"{answer} {extra_text}".strip() if answer else extra_text

            else:
                response = str(response)
                if response:
                    answer = response

        except Exception as exc:
            print(f"response parsing error: {exc}")
            actions = []
            answer = ''

        try:
            # ---- tts ----
            _tts_status = False
            if answer != '':
                st = time.time()
                _time = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())
                _tts_f = f"./tts/{_time}_raw.wav"

                if openrouter_helper.tts_model:
                    _tts_status = openrouter_helper.text_to_speech(
                        answer,
                        _tts_f,
                        TTS_VOICE,
                        response_format='wav',
                        instructions=VOICE_INSTRUCTIONS,
                    )
                    if not _tts_status:
                        gray_print('remote tts unavailable, attempting local Piper/espeak')

                if not _tts_status and resolved_piper_voice:
                    _tts_status = synthesize_with_piper(
                        answer,
                        _tts_f,
                        resolved_piper_voice,
                        resolved_piper_speaker,
                        resolved_piper_length_scale,
                    )

                if not _tts_status:
                    _tts_status = synthesize_with_espeak(answer, _tts_f, TTS_VOICE)

                if _tts_status:
                    tts_file = f"./tts/{_time}_{VOLUME_DB}dB.wav"
                    _tts_status = sox_volume(_tts_f, tts_file, VOLUME_DB)
                gray_print(f'tts takes: {time.time() - st:.3f} s')

            # ---- actions ----
            with action_lock:
                actions_to_be_done = actions
                gray_print(f'actions: {actions_to_be_done}')
                action_status = 'actions'

            # --- sound effects and voice ---
            for _sound in _sound_actions:
                try:
                    sounds_dict[_sound](music)
                except Exception as e:
                    print(f'action error: {e}')

            if _tts_status:
                with speech_lock:
                    speech_loaded = True

            # ---- wait speak done ----
            if _tts_status:
                while True:
                    with speech_lock:
                        if not speech_loaded:
                            break
                    time.sleep(.01)

            # ---- wait actions done ----
            while True:
                with action_lock:
                    if action_status != 'actions':
                        break
                time.sleep(.01)

            ##
            print() # new line

        except Exception as e:
            print(f'actions or TTS error: {e}')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\033[31mERROR: {e}\033[m")
    finally:
        if with_img:
            Vilib.camera_close()
        my_car.reset()

