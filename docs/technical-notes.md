# Technical notes

The investigation found:

- Spanish NTSC VI table: `0x000C9468`
- `yScale[0]`: `0x000C948C`
- `yScale[1]`: `0x000C94A0`
- original `yScale`: `0x400`
- best tested value: `0x4CD`
- region byte: `0x3E`, `P -> E`
- CIC: `7102`
- original CRC: `5F946439 68FA5DD1`

`vStart` changed vertical position only. `yScale` changed vertical size. Values below `0x400` expanded the image; values above `0x400` compressed it. `0x4CD` produced the best tested geometry and was validated on real NTSC hardware.

The patcher refuses unknown ROM revisions rather than patching offsets blindly.
