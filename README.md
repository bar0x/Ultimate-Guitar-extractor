# Ultimate Guitar Extractor & Chordbook Maker

A Python tool to extract chords and tabs from Ultimate Guitar into clean `.txt` files and compile them into a typeset PDF songbook using **Typst**.

## Features

- **CLI Extraction (`ug-extract`):** Fetch one or more tabs directly from Ultimate Guitar URLs, stripping away unnecessary HTML/BBCode tags.
- **Flexible Management:** Supports batch downloads, custom output directories, and automatic file naming.
- **PDF Songbook (In Progress):** Automatic compilation of extracted songs via a Typst template and a dedicated GUI (`ug-gui`) to organize and order your songbook.

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (Python package and project manager)

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/Ultimate-Guitar-extractor.git](https://github.com/YOUR-USERNAME/Ultimate-Guitar-extractor.git)
   cd Ultimate-Guitar-extractor
   ```

2. Sync the virtual environment and install dependencies using `uv`:
   ```bash
   uv sync
   ```

## Usage

### Extract Tabs via CLI (`ug-extract`)

Download a single song into the default folder (`./songs/`):
```bash
uv run ug-extract "https://tabs.ultimate-guitar.com/tab/ed-sheeran/perfect-chords-1956589"
```

Download multiple songs at once into a custom directory:
```bash
uv run ug-extract "URL_1" "URL_2" -o ./my_songbook/
```

Available options (`uv run ug-extract --help`):

| Flag | Description | Default |
| :--- | :--- | :--- |
| `urls` | One or more Ultimate Guitar tab URLs (required) | - |
| `-o`, `--output` | Destination folder for `.txt` files | `./songs/` |
| `-n`, `--name` | Custom output filename (only works with a single URL) | Parsed from URL |
| `-v`, `--verbose` | Enable detailed debug logging | `False` |

## Roadmap

- [x] Ultimate Guitar scraper and CLI extractor (`ug-extract`)
- [ ] PDF songbook compilation powered by `typst`
- [ ] Graphical User Interface for songbook management (`ug-gui`)

## Credits & Licenses

- This project's source code is licensed under the **MIT License** (see the `LICENSE` file for details).
- The included Typst template is based on [Chordish](ORIGINAL_REPO_LINK) by [Author], licensed under the **MIT License**.