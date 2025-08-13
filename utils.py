#!/usr/bin/env python3
# EN: General file helpers (iterate files, path utilities, backups).
# ID: Utilitas berkas umum (iterasi file, utilitas path, cadangan).

import os
import shutil
from typing import Iterable

# EN: Yield files under path matching provided extensions.
# ID: Hasilkan file di bawah path dengan ekstensi tertentu.
def iter_files(path: str, exts: Iterable[str]):
    exts_norm = {e.lower() if e.startswith('.') else f'.{e.lower()}' for e in exts}
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() in exts_norm:
            yield path
        return
    for root, _, files in os.walk(path):
        for fn in files:
            if os.path.splitext(fn)[1].lower() in exts_norm:
                yield os.path.join(root, fn)

# EN: Create a .bak file if requested.
# ID: Buat file .bak jika diminta.
def backup_file(path: str) -> None:
    bak = path + ".bak"
    try:
        shutil.copy2(path, bak)
    except Exception as e:
        print(f"[WARN] Could not create backup {bak}: {e}")

# EN: Ensure mirrored output path under out_dir.
# ID: Pastikan path keluaran mencerminkan struktur di out_dir.
def ensure_out_path(in_path: str, base_in: str, out_dir: str) -> str:
    rel = os.path.relpath(in_path, base_in)
    out_path = os.path.join(out_dir, rel)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    return out_path
