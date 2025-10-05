import base64
import os
import shutil
import time
from io import BytesIO
from typing import Iterable, List, Optional, Union

import requests


# ----------------------------------------------------------------------------
# output helpers
# ----------------------------------------------------------------------------
def chat_print(label: str, message: str) -> None:
    """Consistent timestamped logging for dialogue traffic."""
    width = shutil.get_terminal_size().columns
    msg_len = len(message)
    line_len = max(width - 27, 10)

    if msg_len <= line_len:
        print(f"{time.time():.3f} {label:>6} >>> {message}")
        return

    for idx in range(0, msg_len, line_len):
        chunk = message[idx : idx + line_len]
        if idx == 0:
            print(f"{time.time():.3f} {label:>6} >>> {chunk}")
        else:
            print(f"{'':>26}{chunk}")


# ----------------------------------------------------------------------------
# OpenRouter client wrapper
# ----------------------------------------------------------------------------
class OpenRouterHelper:
    """Utility wrapper for OpenRouter chat, STT, and TTS endpoints."""

    API_BASE = "https://openrouter.ai/api/v1"
    STT_MODEL = "openai/whisper-1"
    TTS_MODEL = "openai/gpt-4o-mini-tts"
    TIMEOUT = 30
    STT_OUT = "stt_output.wav"

    def __init__(
        self,
        api_key: str,
        model: str,
        assistant_name: str,
        system_prompt: Optional[str] = None,
        *,
        timeout: int = TIMEOUT,
        referer: Optional[str] = None,
        site_title: Optional[str] = None,
        stt_model: Optional[str] = None,
        tts_model: Optional[str] = None,
    ) -> None:
        if not api_key:
            raise ValueError("OpenRouter API key is required")
        if not model:
            raise ValueError("OpenRouter chat model is required")

        self.api_key = api_key
        self.model = model
        self.assistant_name = assistant_name
        self.timeout = timeout
        self.referer = referer
        self.site_title = site_title
        self.stt_model = self.STT_MODEL if stt_model is None else stt_model
        self.tts_model = self.TTS_MODEL if tts_model is None else tts_model

        self.messages: List[dict] = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------
    def _headers(self, *, content_type: Optional[str] = "application/json") -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        if content_type:
            headers["Content-Type"] = content_type
        if self.referer:
            headers["HTTP-Referer"] = self.referer
        if self.site_title:
            headers["X-Title"] = self.site_title
        return headers

    def _post_json(self, path: str, payload: dict) -> requests.Response:
        url = f"{self.API_BASE}{path}"
        response = requests.post(
            url,
            headers=self._headers(),
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response

    def _post_multipart(self, path: str, data: dict, files: dict) -> requests.Response:
        url = f"{self.API_BASE}{path}"
        response = requests.post(
            url,
            headers=self._headers(content_type=None),
            data=data,
            files=files,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response

    def _extract_text(self, assistant_message: dict) -> str:
        content = assistant_message.get("content", "")
        if isinstance(content, list):
            parts: List[str] = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text", ""))
            return "".join(parts)
        if isinstance(content, str):
            return content
        return ""

    def _append_history(self, message: dict) -> None:
        self.messages.append(message)

    # ------------------------------------------------------------------
    # speech to text
    # ------------------------------------------------------------------
    def stt(self, audio, language: Union[str, Iterable[str], None] = None) -> Union[str, bool]:
        try:
            wav_data = BytesIO(audio.get_wav_data())
            wav_data.name = self.STT_OUT

            payload = {"model": self.stt_model}
            if language:
                if isinstance(language, str):
                    payload["language"] = language
                else:
                    first = next(iter(language), None)
                    if first:
                        payload["language"] = first
            payload["prompt"] = "This is a conversation between a person and a Picar-X robot."

            response = self._post_multipart(
                "/audio/transcriptions",
                data=payload,
                files={"file": (self.STT_OUT, wav_data, "audio/wav")},
            )
            result = response.json()
            return result.get("text", "")
        except Exception as exc:
            print(f"stt err: {exc}")
            return False

    # ------------------------------------------------------------------
    # dialogue helpers
    # ------------------------------------------------------------------
    def dialogue(self, msg: str) -> Union[dict, str]:
        chat_print("user", msg)
        history = self.messages + [{"role": "user", "content": msg}]
        response = self._post_json(
            "/chat/completions",
            payload={
                "model": self.model,
                "messages": history,
            },
        )

        payload = response.json()
        choice = payload.get("choices", [{}])[0]
        message = choice.get("message", {})
        text = self._extract_text(message)
        chat_print(self.assistant_name, text)

        self.messages = history
        self._append_history(message)

        try:
            return eval(text)
        except Exception:
            return text

    def dialogue_with_img(self, msg: str, img_path: str) -> Union[dict, str]:
        chat_print("user", msg)

        with open(img_path, "rb") as f_img:
            b64_img = base64.b64encode(f_img.read()).decode("utf-8")

        content = [
            {"type": "text", "text": msg},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64_img}",
                    "detail": "auto",
                },
            },
        ]

        history = self.messages + [{"role": "user", "content": content}]

        response = self._post_json(
            "/chat/completions",
            payload={
                "model": self.model,
                "messages": history,
            },
        )

        payload = response.json()
        choice = payload.get("choices", [{}])[0]
        message = choice.get("message", {})
        text = self._extract_text(message)
        chat_print(self.assistant_name, text)

        self.messages = history
        self._append_history(message)

        try:
            return eval(text)
        except Exception:
            return text

    # ------------------------------------------------------------------
    # text to speech
    # ------------------------------------------------------------------
    def text_to_speech(
        self,
        text: str,
        output_file: str,
        voice: str = "alloy",
        response_format: str = "mp3",
        speed: float = 1.0,
        instructions: str = "",
    ) -> bool:
        if not self.tts_model:
            return False
        try:
            directory = os.path.dirname(output_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            response = requests.post(
                f"{self.API_BASE}/audio/speech",
                headers={
                    **self._headers(),
                    "Accept": "application/octet-stream",
                },
                json={
                    "model": self.tts_model,
                    "input": text,
                    "voice": voice,
                    "response_format": response_format,
                    "speed": speed,
                    "instructions": instructions,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()

            with open(output_file, "wb") as f_out:
                f_out.write(response.content)
            return True
        except Exception as exc:
            print(f"tts err: {exc}")
            return False


__all__ = ["OpenRouterHelper"]
