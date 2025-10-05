## Picar-X GPT examples usage

----------------------------------------------------------------

## Install dependencies

- Ensure the base Picar-X stack (Pidog, Robot HAT libraries, etc.) is installed first.
  <https://docs.sunfounder.com/projects/picar-x-v20/en/latest/python/python_start/install_all_modules.html>

- Install speech and HTTP helpers

> [!NOTE]
When using pip install outside of a virtual environment you may need to add the `"--break-system-packages"` flag.

```bash
sudo pip3 install -U requests --break-system-packages
sudo pip3 install -U SpeechRecognition --break-system-packages
sudo pip3 install -U piper-tts --break-system-packages

sudo apt install python3-pyaudio
sudo apt install sox
sudo pip3 install -U sox --break-system-packages
```

To enable higher-quality offline speech, download a Piper voice and point `PIPER_VOICE_PATH` to it. Example (replace the URL with your preferred voice):

```bash
mkdir -p ~/picar-x/gpt_examples/voices
curl -L -o ~/picar-x/gpt_examples/voices/en_US-amy-low.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/low/en_US-amy-low.onnx
curl -L -o ~/picar-x/gpt_examples/voices/en_US-amy-low.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/low/en_US-amy-low.onnx.json
```

----------------------------------------------------------------

## Configure OpenRouter access

1. Create an API key at <https://openrouter.ai/keys> and copy it into `OPENROUTER_API_KEY` inside `gpt_examples/keys.py`.
2. Pick a chat model (for example `openai/gpt-4o-mini` or `google/gemini-flash-1.5`) and set `OPENROUTER_MODEL`.
3. Optionally set `OPENROUTER_REFERER` and `OPENROUTER_SITE_TITLE` so your traffic is attributed correctly in the OpenRouter dashboard.
4. Adjust `OPENROUTER_TTS_MODEL` and `OPENROUTER_STT_MODEL` if you want non-default audio backends supported by OpenRouter.

The default system prompt in `OPENROUTER_SYSTEM_PROMPT` already nudges the assistant to respond with a Python dict containing `actions` and `answer`, which keeps the demo logic unchanged.

----------------------------------------------------------------

## Run

- Voice controlled mode

```bash
sudo python3 gpt_car.py
```

- Voice input with an alternate Piper voice

```bash
sudo python3 gpt_car.py --voice-path voices/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx
```

- Keyboard input mode

```bash
sudo python3 gpt_car.py --keyboard
```

- Run without uploading camera frames

```bash
sudo python3 gpt_car.py --keyboard --no-img
```

> [!WARNING]
You must run the examples with `sudo`, otherwise the speaker may remain muted.
Some Robot HAT revisions also need `pinctrl set 20 op dh` or `robot-hat enable_speaker` before playback.

----------------------------------------------------------------

## Tuning options

- **STT language filter** – tweak the `LANGUAGE` list in `gpt_car.py` to bias transcription towards specific locales.
- **TTS gain** – change `VOLUME_DB` in `gpt_car.py` to increase or reduce post-processing volume (values above `5` may distort).
- **Voice selection** – set `TTS_VOICE` to any voice supported by the configured TTS model (for example `alloy`, `echo`, `nova`). When falling back to local `espeak`, unsupported names automatically map to the default English voice.
- **Voice style** – customise `VOICE_INSTRUCTIONS` to steer generated speech tone.
- **TTS backend** – leave `OPENROUTER_TTS_MODEL` populated to call the OpenRouter `/audio/speech` endpoint, set it to an empty string to skip the network call, and fill in `PIPER_VOICE_PATH` (plus optional `PIPER_SPEAKER_ID` / `PIPER_LENGTH_SCALE`) for Piper-based synthesis. If Piper is unavailable, the script finally falls back to `espeak`.
- **Runtime voice override** – add `--voice-path /path/to/model.onnx` to the launch command to try a different Piper voice without editing `keys.py`. Relative paths resolve from `gpt_examples/`.

----------------------------------------------------------------

## Piper voice reference

| Alias | Voice path (relative to `gpt_examples/`) | Accent / Notes |
| --- | --- | --- |
| `amy` | `voices/en/en_US/amy/low/en_US-amy-low.onnx` | US female, fast to synthesize |
| `lessac` | `voices/en/en_US/lessac/low/en_US-lessac-low.onnx` | US neutral narrator tone |
| `southern_english_female` | `voices/en/en_GB/southern_english_female/low/en_GB-southern_english_female-low.onnx` | UK southern female |

Switch voices at launch with `--voice-path voices/.../model.onnx`, or set `PIPER_VOICE_PATH` in `keys.py` for a permanent default.

```python
# OpenRouter assistant init
# =================================================================
openrouter_helper = OpenRouterHelper(
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    'picarx',
    system_prompt=OPENROUTER_SYSTEM_PROMPT,
    referer=OPENROUTER_REFERER or None,
    site_title=OPENROUTER_SITE_TITLE or None,
    stt_model=OPENROUTER_STT_MODEL or None,
    tts_model=OPENROUTER_TTS_MODEL or None,
)
```

----------------------------------------------------------------

## Preset actions

`preset_actions.py` contains helper functions such as `shake_head`, `nod`, `depressed`, `honking`, and `start_engine`. Run it directly to preview available moves:

```bash
python3 preset_actions.py
```
