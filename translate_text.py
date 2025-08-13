#!/usr/bin/env python3
# EN: CLI script for plain-text/markdown files. Translates entire content.
# ID: Skrip CLI untuk file teks/markdown. Menerjemahkan seluruh isi.

import os
import argparse
from typing import Optional

from deepl_client import translate_text, load_api_key, DEFAULT_API_URL
from utils import iter_files, backup_file, ensure_out_path

# EN: Process whole text content at once (still chunked internally).
# ID: Proses keseluruhan isi teks sekaligus (tetap dipecah internal).
def process_content(
    content: str,
    *,
    api_url: str,
    api_key: str,
    target_lang: str,
    source_lang: Optional[str],
    delay: float,
    max_length: int,
) -> str:
    return translate_text(
        content,
        api_url=api_url,
        api_key=api_key,
        target_lang=target_lang,
        source_lang=source_lang,
        delay=delay,
        max_length=max_length,
    )

# EN: CLI entrypoint for text/markdown files.
# ID: Titik masuk CLI untuk file teks/markdown.
def main() -> int:
    p = argparse.ArgumentParser(description="Translate text/markdown files using DeepL")
    p.add_argument("--path", required=True, help="File or directory to process")
    p.add_argument("--ext", nargs="+", default=[".txt", ".md"], help="Extensions to include")
    p.add_argument("--target-lang", default="EN", help="Target language code (e.g., EN, ID, JA)")
    p.add_argument("--source-lang", default=None, help="Source language code (optional)")
    p.add_argument("--api-url", default=DEFAULT_API_URL, help="DeepL API URL")
    p.add_argument("--delay", type=float, default=1.0, help="Delay between requests (sec)")
    p.add_argument("--max-length", type=int, default=4500, help="Chunk size (chars)")
    p.add_argument("--in-place", action="store_true", help="Edit files in place (create .bak)")
    p.add_argument("--out-dir", default=None, help="Output directory if not in-place")
    p.add_argument("--no-backup", action="store_true", help="Do not create .bak when in-place")

    args = p.parse_args()

    try:
        api_key = load_api_key()
    except Exception as e:
        print(f"[ERROR] {e}")
        return 2

    base_path = os.path.abspath(args.path)
    if not args.in_place and not args.out_dir:
        print("[ERROR] Either use --in-place or provide --out-dir")
        return 2
    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)

    files = list(iter_files(base_path, args.ext))
    if not files:
        print("[INFO] No files matched.")
        return 0

    error_log_path = os.path.join(os.getcwd(), "error_log.txt")

    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = process_content(
                content,
                api_url=args.api_url,
                api_key=api_key,
                target_lang=args.target_lang,
                source_lang=args.source_lang,
                delay=args.delay,
                max_length=args.max_length,
            )
            if args.in_place:
                if not args.no_backup:
                    backup_file(fp)
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✅ Updated in place: {fp}")
            else:
                out_path = ensure_out_path(
                    fp,
                    base_in=base_path if os.path.isdir(base_path) else os.path.dirname(base_path),
                    out_dir=args.out_dir,
                )
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"📄 Wrote: {out_path}")
        except Exception as e:
            print(f"⚠ Failed to process {fp}: {e}")
            try:
                with open(error_log_path, "a", encoding="utf-8") as logf:
                    logf.write(f"{fp} : {e}\n")
            except Exception:
                pass
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
