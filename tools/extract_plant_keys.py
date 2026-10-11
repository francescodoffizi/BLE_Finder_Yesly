#!/usr/bin/env python3
"""Extract Finder YESLY plant topology, devices, MACs, and AES-128 keys from plant_dump.bin.

Saves output to local keys.json (which is gitignored).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from proto import parse_fields


def extract_plant(dump_path: str) -> dict:
    with open(dump_path, "rb") as f:
        data = f.read()

    top = parse_fields(data)
    if 3 not in top:
        raise ValueError("Field 3 not found in plant dump")

    plant = parse_fields(top[3][0])

    # 1. Device hardware info from Field 12
    devices_hw: dict[str, dict] = {}
    for item in plant.get(12, []):
        sub = parse_fields(item)
        uuid = sub.get(1, [b""])[0].decode(errors="ignore")
        family = sub.get(3, [b""])[0].decode(errors="ignore")
        f4 = sub.get(4, [b""])[0]
        mac = ""
        if isinstance(f4, bytes):
            mac = parse_fields(f4).get(1, [b""])[0].decode(errors="ignore")

        raw_f5 = sub.get(5, [b""])[0]
        f5_hex = raw_f5.hex() if isinstance(raw_f5, bytes) else ""

        f6 = sub.get(6, [b""])[0]
        config = {}
        if isinstance(f6, bytes):
            try:
                # First byte is length/tag, followed by json
                s = f6.decode("utf-8", errors="ignore")
                idx = s.find("{")
                if idx != -1:
                    config = json.loads(s[idx:])
            except Exception:
                pass

        gateway_uuid = ""
        f8 = sub.get(8, [b""])[0]
        if isinstance(f8, bytes):
            gateway_uuid = parse_fields(f8).get(1, [b""])[0].decode(errors="ignore")

        devices_hw[uuid] = {
            "uuid": uuid,
            "mac": mac,
            "family": family,
            "f5_hex": f5_hex,
            "gateway_uuid": gateway_uuid,
            "config": config,
        }

    # 2. AES-128 Keys from Field 11
    keys_by_target: dict[str, dict[str, str]] = {}
    for item in plant.get(11, []):
        sub = parse_fields(item)
        k_type = sub.get(2, [b""])[0].decode(errors="ignore")
        k_id = sub.get(1, [b""])[0].decode(errors="ignore")
        f3 = sub.get(3, [b""])
        target_uuid = ""
        if f3 and isinstance(f3[0], bytes):
            inner = parse_fields(f3[0])
            target_uuid = inner.get(1, [b""])[0].decode(errors="ignore")

        raw_key = sub.get(7, [b""])[0]
        key_hex = raw_key.hex() if isinstance(raw_key, bytes) else ""

        if target_uuid:
            keys_by_target.setdefault(target_uuid, {})[k_type] = key_hex

    # 3. User friendly names & rooms from Field 15
    items_msg = plant.get(15, [None])[0]
    entities: list[dict] = []
    if items_msg and isinstance(items_msg, bytes):
        sub = parse_fields(items_msg)
        for elem in sub.get(3, []):
            if not isinstance(elem, bytes):
                continue
            f = parse_fields(elem)
            name = f.get(7, [b""])[0].decode(errors="replace")
            elem_id = f.get(1, [b""])[0].decode(errors="replace")
            t8 = f.get(8, [b""])[0]
            dev_type = ""
            if isinstance(t8, bytes):
                dev_type = parse_fields(t8).get(1, [b""])[0].decode(errors="replace")

            dev_msg = f.get(2, [b""])[0]
            dev_uuid = ""
            if isinstance(dev_msg, bytes):
                dev_uuid = parse_fields(dev_msg).get(1, [b""])[0].decode(errors="replace")

            channel = f.get(3, [1])[0]
            if not isinstance(channel, int):
                channel = 1

            hw = devices_hw.get(dev_uuid, {})
            keys = keys_by_target.get(dev_uuid, {})

            entities.append({
                "name": name,
                "type": dev_type,
                "elem_id": elem_id,
                "device_uuid": dev_uuid,
                "channel": channel,
                "family": hw.get("family", ""),
                "mac": hw.get("mac", ""),
                "f5_hex": hw.get("f5_hex", ""),
                "config": hw.get("config", {}),
                "keys": keys,
            })

    return {
        "plant_id": plant.get(1, [b""])[0].decode(errors="ignore"),
        "plant_name": plant.get(2, [b""])[0].decode(errors="ignore"),
        "entities": entities,
        "raw_devices_hw": devices_hw,
    }


def main():
    dump_file = sys.argv[1] if len(sys.argv) > 1 else "/root/workspace/plant_dump.bin"
    output_file = Path(__file__).resolve().parent.parent / "keys.json"

    print(f"Reading plant dump from {dump_file}...")
    result = extract_plant(dump_file)

    print(f"Plant: {result['plant_name']} ({result['plant_id']})")
    print(f"Extracted {len(result['entities'])} entities.")

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    # Secure file permissions (rw-------)
    os.chmod(output_file, 0o600)
    print(f"Saved secure plant keys to: {output_file} (permissions 0600, gitignored)")


if __name__ == "__main__":
    main()
