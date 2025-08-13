#!/usr/bin/env python3
# EN: Core DeepL client utilities: env/config loading, chunking, request with retries.
# ID: Utilitas inti DeepL: muat env/konfigurasi, pemecahan teks, dan request dengan retry.

import os
import time
import requests
from typing import List, Optional

# EN: Try load from .env if python-dotenv is installed; safe to ignore if not.
# ID: Coba muat dari .env jika python-dotenv terpasang; aman diabaikan jika tidak ada.
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

# EN: Optional fallback to config.py (define DEEPL_API_KEY there).
# ID: Opsi cadangan ke config.py (definisikan DEEPL_API_KEY di sana).
try:
    from config import DEEPL_API_KEY as CONFIG_DEEPL_API_KEY  # type: ignore
except Exception:
    CONFIG_DEEPL_API_KEY = None  # type: ignore

DEFAULT_API_URL = "https://api-free.deepl.com/v2/translate"


# EN: Split long text into smaller chunks to fit API limits.
# ID: Pecah teks panjang menjadi potongan kecil agar sesuai batas API.
def chunk_text(text: str, max_length: int = 4500) -> List[str]:
    text = text.strip()
    if not text:
        return []
    chunks: List[str] = []
    while len(text) > max_length:
        split_pos = text.rfind(" ", 0, max_length)
        if split_pos == -1:
            split_pos = max_length
        chunks.append(text[:split_pos])
        text = text[split_pos:].lstrip()
    if text:
        chunks.append(text)
    return chunks


# EN: Perform one DeepL POST request.
# ID: Melakukan satu permintaan POST ke DeepL.
def _post_deepl(
    api_url: str,
    api_key: str,
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    timeout: int = 20,
) -> str:
    data = {"auth_key": api_key, "text": text, "target_lang": target_lang}
    if source_lang:
        data["source_lang"] = source_lang
    resp = requests.post(api_url, data=data, timeout=timeout)
    resp.raise_for_status()
    payload = resp.json()
    if isinstance(payload, dict) and "translations" in payload:
        return payload["translations"][0]["text"]
    return text


# EN: High-level translate with chunking, delay, and retries.
# ID: Terjemahan level-tinggi dengan chunking, jeda, dan retry.
def translate_text(
    text: str,
    *,
    api_url: str,
    api_key: str,
    target_lang: str,
    source_lang: Optional[str],
    delay: float,
    max_length: int,
    max_retries: int = 4,
    backoff_base: float = 1.5,
) -> str:
    if not text.strip():
        return text
    pieces = chunk_text(text, max_length=max_length)
    out: List[str] = []
    for p in pieces:
        attempt = 0
        while True:
            try:
                translated = _post_deepl(api_url, api_key, p, target_lang, source_lang)
                out.append(translated)
                if delay > 0:
                    time.sleep(delay)
                break
            except requests.HTTPError as http_err:
                attempt += 1
                if attempt > max_retries:
                    print(f"[!] HTTP error after {attempt} attempts: {http_err}")
                    out.append(p)
                    break
                sleep_for = backoff_base ** attempt
                print(f"[!] HTTP error: {http_err}; retrying in {sleep_for:.1f}s…")
                time.sleep(sleep_for)
            except Exception as e:
                attempt += 1
                if attempt > max_retries:
                    print(f"[!] Error after {attempt} attempts: {e}")
                    out.append(p)
                    break
                sleep_for = backoff_base ** attempt
                print(f"[!] Error: {e}; retrying in {sleep_for:.1f}s…")
                time.sleep(sleep_for)
    return " ".join(out)


# EN: Load API key from env or config.py; raise if missing.
# ID: Ambil API key dari env atau config.py; error jika tidak ada.
def load_api_key() -> str:
    api_key = os.getenv("DEEPL_API_KEY") or CONFIG_DEEPL_API_KEY
    if not api_key:
        raise RuntimeError("DEEPL_API_KEY not found. Set environment variable or config.py")
    return api_key
