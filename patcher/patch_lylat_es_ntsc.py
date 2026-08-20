#!/usr/bin/env python3
from pathlib import Path
import argparse, struct, ipl3checksum

NTSC_TABLE = 0x000C9468
YSCALE_0 = NTSC_TABLE + 0x24
YSCALE_1 = NTSC_TABLE + 0x38
EXPECTED_YSCALE = 0x400
TARGET_YSCALE = 0x4CD
EXPECTED_CRC1 = 0x5F946439
EXPECTED_CRC2 = 0x68FA5DD1
EXPECTED_REGION = 0x50
TARGET_REGION = 0x45

def ru32(data, off):
    return struct.unpack(">I", data[off:off+4])[0]

def wu32(data, off, value):
    data[off:off+4] = struct.pack(">I", value & 0xffffffff)

def main():
    p = argparse.ArgumentParser(description="Lylat Wars ES PAL -> NTSC 60 Hz")
    p.add_argument("rom", type=Path)
    p.add_argument("-o", "--output", type=Path)
    p.add_argument("--yscale", type=lambda x: int(x,0), default=TARGET_YSCALE)
    a = p.parse_args()

    src = a.rom.expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"Input ROM not found: {src}")
    dst = a.output.expanduser().resolve() if a.output else src.with_name(src.stem + "_NTSC_60Hz.z64")

    data = bytearray(src.read_bytes())
    if data[:4] != bytes.fromhex("80371240"):
        raise SystemExit("ROM must be .z64 big-endian format.")

    crc1, crc2 = ru32(data,0x10), ru32(data,0x14)
    region = data[0x3E]
    y0, y1 = ru32(data,YSCALE_0), ru32(data,YSCALE_1)

    if (crc1,crc2) != (EXPECTED_CRC1,EXPECTED_CRC2):
        raise SystemExit(f"Unsupported ROM revision. Expected CRC {EXPECTED_CRC1:08X} {EXPECTED_CRC2:08X}.")
    if region != EXPECTED_REGION:
        raise SystemExit("Unexpected region byte; expected PAL 'P' (0x50).")
    if (y0,y1) != (EXPECTED_YSCALE,EXPECTED_YSCALE):
        raise SystemExit("Unexpected yScale values.")

    data[0x3E] = TARGET_REGION
    wu32(data,YSCALE_0,a.yscale)
    wu32(data,YSCALE_1,a.yscale)

    cic = ipl3checksum.detectCIC(data)
    n1,n2 = ipl3checksum.calculateChecksumAutodetect(data)
    wu32(data,0x10,n1); wu32(data,0x14,n2)
    dst.write_bytes(data)

    print(f"CIC: {cic}")
    print(f"yScale: 0x{a.yscale:08X}")
    print(f"CRC: {n1:08X} {n2:08X}")
    print(f"Output: {dst}")

if __name__ == "__main__":
    main()
