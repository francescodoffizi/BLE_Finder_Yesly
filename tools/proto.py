"""Minimal protobuf varint + length-delimited field encoder/decoder."""

from __future__ import annotations


def parse_varint(data: bytes, pos: int) -> tuple[int, int]:
    """Read a varint at pos; return (value, new_pos)."""
    result = 0
    shift = 0
    while True:
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result, pos
        shift += 7


def parse_fields(data: bytes) -> dict[int, list]:
    """Parse a protobuf message into a dict of {field_number: [values]}."""
    pos = 0
    out: dict[int, list] = {}
    while pos < len(data):
        tag, pos = parse_varint(data, pos)
        field = tag >> 3
        wire = tag & 7
        if wire == 0:  # varint
            v, pos = parse_varint(data, pos)
        elif wire == 2:  # length-delimited
            length, pos = parse_varint(data, pos)
            v = data[pos : pos + length]
            pos += length
        else:
            raise ValueError(f"unsupported wire type {wire}")
        out.setdefault(field, []).append(v)
    return out
