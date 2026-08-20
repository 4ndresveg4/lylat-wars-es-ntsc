# Technical Notes

This document describes the investigation behind the PAL-to-NTSC conversion used by this project.

The goal was not simply to change the ROM region. The objective was to preserve the original Spanish localization — including text and voices — while obtaining correct NTSC 60 Hz video output and maintaining the original gameplay behavior.

## 1. Source ROM

The supported Spanish PAL ROM uses:

- Region code: `P`
- Region byte offset: `0x3E`
- CIC: `7102`
- Original CRC1: `5F946439`
- Original CRC2: `68FA5DD1`

The patcher validates the supported ROM revision before modifying it. Unknown revisions are rejected instead of applying hardcoded offsets blindly.

## 2. Initial PAL → NTSC conversion

Changing the region byte:

    Offset: 0x3E
    P -> E

allowed the Spanish ROM to operate as an NTSC title.

However, this alone did not produce correct video geometry.

The game ran at NTSC speed, but the rendered image remained vertically incorrect.

This demonstrated that the region identifier was only part of the conversion.

## 3. Video Interface investigation

The investigation then focused on the Nintendo 64 Video Interface (VI) configuration.

The relevant table identified in the Spanish ROM begins at:

    0x000C9468

The relevant vertical scaling values were located at:

    yScale[0] = 0x000C948C
    yScale[1] = 0x000C94A0

Both originally contained:

    0x00000400

## 4. vStart vs. yScale

Several experimental ROMs were generated to determine which VI parameters controlled the observed problem.

Testing showed two different behaviors:

    vStart -> vertical position
    yScale -> vertical size

Changing `vStart` moved the picture vertically but did not correct its geometry.

Changing `yScale`, however, changed the vertical size of the rendered image.

This isolated `yScale` as the parameter responsible for the remaining PAL-to-NTSC geometry problem.

## 5. yScale experiments

The original value was:

    0x400

Experimental values demonstrated that:

    yScale < 0x400 -> image expands vertically
    yScale > 0x400 -> image compresses vertically

Several ROM variants were generated and tested rather than assuming a value mathematically.

The best tested result was:

    yScale = 0x4CD

This value corrected the vertical geometry while preserving the expected NTSC behavior.

## 6. Checksum correction

Modifying executable/video configuration data changes the ROM and therefore requires valid Nintendo 64 header checksums.

CIC autodetection identified the Spanish ROM as:

    CIC 7102

The original header contained:

    CRC1 = 5F946439
    CRC2 = 68FA5DD1

After applying the modifications, CRC1 and CRC2 are recalculated for the modified ROM rather than retaining the original checksum values.

This was important because using an incorrect CIC algorithm can produce invalid checksums even when the actual patch data is correct.

## 7. Final conversion

The final patching process therefore performs the following operations:

1. Validate the supported Spanish PAL ROM.
2. Change the region byte from `P` to `E`.
3. Change both relevant `yScale` values from `0x400` to `0x4CD`.
4. Recalculate the Nintendo 64 CRC1/CRC2 using the correct CIC.
5. Write a new patched ROM without modifying the user's original file.

## 8. Validation

The resulting ROM was tested in:

- Project64
- Real Nintendo 64 hardware
- Super 64 flash cartridge
- NTSC video output

Testing covered more than the title screen.

The following were checked:

- title screen
- menus
- intro sequence
- Spanish subtitles/text
- Spanish voice audio
- gameplay
- HUD rendering
- vertical screen geometry
- gameplay speed

The resulting version retained the Spanish localization while operating correctly in the tested NTSC environment.

## 9. Main finding

The central technical finding of the investigation was that a PAL-to-NTSC conversion for this ROM could not be treated only as a region-byte patch.

The practical relationship discovered during testing was:

    Region byte -> NTSC/PAL identification
    vStart      -> vertical position
    yScale      -> vertical size
    CRC         -> ROM integrity after modification

For the supported Spanish ROM revision, the hardware-tested configuration used by this project is:

    Region: P -> E
    yScale: 0x400 -> 0x4CD
    CIC:     7102

## 10. Safety

The patcher does not contain or distribute the original game ROM.

Users must provide their own supported ROM dump.

The tool validates the input revision and refuses unknown ROMs rather than applying offsets to an incompatible file.
