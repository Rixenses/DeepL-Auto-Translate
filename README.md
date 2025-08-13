# DeepL Auto Translate

**EN:** A simple, flexible toolkit to translate files using the DeepL API.
**ID:** Skrip sederhana dan fleksibel untuk menerjemahkan file menggunakan DeepL API.

---

## Created by / Dibuat oleh:
- **Ariq S. F. 'Rixenses' Ibrahim**

---

## Features / Fitur

- **EN:** Two CLIs:
  - `translate_xml.py`: translate only the text between tags (XML/HTML-like), preserve tags, optionally keep `<!-- ... -->` comments.
  - `translate_text.py`: translate entire text/Markdown files.
- **ID:** Dua CLI:
  - `translate_xml.py`: hanya menerjemahkan teks di antara tag (XML/HTML-dll), tag tetap utuh, komentar `<!-- ... -->` bisa dibiarkan.
  - `translate_text.py`: menerjemahkan seluruh isi file teks/Markdown.

- **EN:** Works on Windows/Mac/Linux, supports in-place editing (with `.bak` backup) or writing to an output directory.
- **ID:** Berjalan di Windows/Mac/Linux, mendukung edit langsung (dengan cadangan `.bak`) atau tulis ke folder output.

- **EN:** Chunking, retry with exponential backoff, simple rate limiting.
- **ID:** Pemecahan teks, retry dengan backoff eksponensial, dan pembatasan laju sederhana.

---

## Requirements / Kebutuhan

- Python 3.8+
- `requests`
- `python-dotenv` (optional, for `.env`)

---

## How to Run / Cara Menjalankan

### [I] Preparation / Persiapan
1. **Install Python** (version 3.8+)
2. **Install dependencies / Install dependensi**
3. **Set your DeepL API Key / Pasang API Key DeepL**

### [II] Running the scripts / Menjalankan skrip
#### a) XML/HTML-like files
#### EN: Translates only text between tags, keeps tags intact.
#### ID: Hanya menerjemahkan teks di antara tag, tag tetap utuh.
#### Example/Contoh:
python translate_xml.py --path ./source_folder --ext .xml .html \
    --target-lang ID --in-place --keep-comments
#### Options/Opsi:
--path → file or folder to process / file atau folder yang diproses.
--ext → file extensions / ekstensi file.
--target-lang → target language code / kode bahasa tujuan.
--in-place → edit original files / edit file asli.
--keep-comments → keep <!-- ... --> comments / biarkan komentar tetap.

#### b) Plain text / Markdown
#### EN: Translates entire file content.
#### ID: Menerjemahkan seluruh isi file.
#### Example/Contoh:
bash
Copy
Edit
python translate_text.py --path ./docs --ext .txt .md \
    --target-lang EN --out-dir ./translated
#### Options/Opsi:
--out-dir → output folder / folder hasil terjemahan.

### [III] Target Language Codes / Kode Bahasa Tujuan
#### EN: You can use the following codes:
#### ID: Anda bisa menggunakan kode bahasa berikut:
| Code  | Language / Bahasa                         |
| ----- | ----------------------------------------- |
| BG    | Bulgarian / Bulgaria                      |
| CS    | Czech / Ceko                              |
| DA    | Danish / Denmark                          |
| DE    | German / Jerman                           |
| EL    | Greek / Yunani                            |
| EN    | English / Inggris                         |
| EN-GB | English (UK)                              |
| EN-US | English (US)                              |
| ES    | Spanish / Spanyol                         |
| ET    | Estonian / Estonia                        |
| FI    | Finnish / Finlandia                       |
| FR    | French / Perancis                         |
| HU    | Hungarian / Hungaria                      |
| ID    | Indonesian / Indonesia                    |
| IT    | Italian / Italia                          |
| JA    | Japanese / Jepang                         |
| KO    | Korean / Korea                            |
| LT    | Lithuanian / Lituania                     |
| LV    | Latvian / Latvia                          |
| NB    | Norwegian Bokmål                          |
| NL    | Dutch / Belanda                           |
| PL    | Polish / Polandia                         |
| PT    | Portuguese / Portugis                     |
| PT-BR | Portuguese (Brazil)                       |
| RO    | Romanian / Rumania                        |
| RU    | Russian / Rusia                           |
| SK    | Slovak / Slovakia                         |
| SL    | Slovenian / Slovenia                      |
| SV    | Swedish / Swedia                          |
| TR    | Turkish / Turki                           |
| UK    | Ukrainian / Ukraina                       |
| ZH    | Chinese (Simplified) / Mandarin Sederhana |

Note / Catatan:
For DeepL Pro, use --api-url https://api.deepl.com/v2/translate
Untuk DeepL Pro, gunakan --api-url https://api.deepl.com/v2/translate

---
