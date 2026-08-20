# Lylat Wars ES PAL → NTSC 60 Hz

A Python-based ROM patcher for a specific Spanish PAL release of **Lylat Wars (Nintendo 64)**.

The project converts the supported Spanish PAL ROM to **NTSC / 60 Hz** while preserving the original **Spanish text and voices**, correcting the vertical video geometry, and recalculating the Nintendo 64 ROM checksums.

The conversion was developed through binary analysis, controlled video-parameter experiments, emulator testing, and validation on real Nintendo 64 hardware.

---

## The problem

Simply changing the Spanish PAL ROM region to NTSC is not enough.

The game can operate at NTSC speed, but the PAL video configuration produces incorrect vertical geometry when used as NTSC.

During the investigation, the relevant Nintendo 64 Video Interface parameters were isolated and tested individually.

The important distinction was:

    Region byte -> PAL / NTSC identification
    vStart      -> vertical position
    yScale      -> vertical size
    CRC1/CRC2   -> ROM integrity after modification

Testing showed that changing `vStart` only moved the image vertically.

The remaining geometry problem was controlled by `yScale`.

---

## The solution

For the supported Spanish ROM revision, the final tested configuration is:

    Region: P -> E
    yScale: 0x400 -> 0x4CD
    CIC: 7102

The patcher performs the required modifications automatically and recalculates the Nintendo 64 CRC1/CRC2 values afterward.

The resulting ROM preserves:

- Spanish text
- Spanish voices/audio
- NTSC 60 Hz operation
- Corrected vertical geometry
- Original gameplay speed

The original input ROM is never overwritten.

---

## What the patcher changes

| Component | Original | Patched |
|---|---|---|
| Region byte | `P (0x50)` | `E (0x45)` |
| NTSC `yScale` | `0x400` | `0x4CD` |
| CRC1 / CRC2 | Original values | Recalculated |
| Spanish text | Preserved | Preserved |
| Spanish voices | Preserved | Preserved |

CRC calculation uses automatic CIC detection.

---

## Supported base ROM

The patcher currently supports the tested Spanish PAL revision with the following characteristics:

    Format: .z64 (big-endian)
    CRC1: 5F946439
    CRC2: 68FA5DD1
    Region: P
    CIC: 7102

The patcher validates the input ROM before modifying it.

Unknown or unsupported revisions are rejected rather than applying hardcoded offsets blindly.

**No ROM is included in this repository.**

---

## Requirements

- Python 3
- A supported `.z64` dump of the Spanish PAL game

Install the Python dependencies with:

    python3 -m pip install -r requirements.txt

---

## Usage

Run:

    python3 patcher/patch_lylat_es_ntsc.py "/path/to/Lylat wars 64 [Esp].z64"

For example:

    python3 patcher/patch_lylat_es_ntsc.py "/home/user/roms/Lylat wars 64 [Esp].z64"

The patched ROM is written as a new file:

    Lylat wars 64 [Esp]_NTSC_60Hz.z64

The source ROM remains unchanged.

---

## PAL → NTSC video correction

Changing the Spanish PAL ROM to NTSC was not enough by itself.

The game could run at 60 Hz, but the original PAL vertical configuration produced incorrect vertical scaling/positioning on NTSC output.

### Before — incorrect vertical geometry

| Test 1 | Test 2 | Test 3 |
|---|---|---|
| ![](docs/images/staefoxfallo1.png) | ![](docs/images/staefoxfallo2.png) | ![](docs/images/staefoxfallo3.png) |

### After — corrected NTSC output

| Test 1 | Test 2 | Test 3 |
|---|---|---|
| ![](docs/images/staefoxcrrecto1.png) | ![](docs/images/staefoxcrrecto2.png) | ![](docs/images/staefoxcrrecto3.png) |

The final solution uses the tested `yScale = 0x4CD` configuration and recalculates the N64 ROM checksums.

---

## Validation

The resulting ROM was tested using:

- Project64
- Real Nintendo 64 NTSC hardware
- Super 64 flash cartridge
- NTSC television

Testing covered:

- Title screen
- Menus
- Intro sequence
- Spanish subtitles/text
- Spanish voice audio
- Gameplay
- HUD rendering
- Vertical screen geometry
- Gameplay speed

The final version operated correctly in the tested NTSC environment while retaining the Spanish localization.

---

## Technical investigation

The project was developed by comparing ROM behavior and experimentally isolating the video parameters responsible for the PAL/NTSC differences.

Relevant findings include:

    Spanish NTSC VI table: 0x000C9468

    yScale[0]: 0x000C948C
    yScale[1]: 0x000C94A0

    Original yScale: 0x400
    Tested final value: 0x4CD

Experimental testing established:

    vStart -> changes vertical position
    yScale -> changes vertical size

Values below `0x400` expanded the image vertically, while values above `0x400` compressed it.

The tested `0x4CD` configuration produced the best geometry and was subsequently validated on real NTSC Nintendo 64 hardware.

For the complete investigation, see:

**[Technical Notes](docs/technical-notes.md)**

---

## Project structure

    lylat-wars-es-ntsc/
    |
    |-- patcher/
    |   `-- patch_lylat_es_ntsc.py
    |
    |-- docs/
    |   |-- technical-notes.md
    |   |-- compatibility.md
    |   `-- images/
    |
    |-- requirements.txt
    |-- LICENSE
    |-- .gitignore
    `-- README.md

---

## Safety

The patcher checks that the input corresponds to the supported ROM revision before modifying known offsets.

This prevents the tool from blindly patching an unknown ROM revision.

The original ROM is not modified. A separate patched file is generated.

---

## Legal

This repository contains **no commercial ROMs, game audio, extracted graphics, or other copyrighted game assets required to play the game**.

Users must provide their own legally obtained ROM dump.

This project provides only the code and technical information necessary to reproduce the PAL-to-NTSC modification.

---

## Status

**Working and hardware tested.**

Spanish PAL → NTSC 60 Hz conversion has been successfully validated in Project64 and on real Nintendo 64 NTSC hardware using a Super 64 flash cartridge.
