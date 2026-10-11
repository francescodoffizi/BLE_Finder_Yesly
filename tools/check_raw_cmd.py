from custom_components.finder_you.api.proto import field_string, field_varint

def build_switch_body(plant_id, device_uuid, channel):
    return (
        field_string(2, plant_id)
        + field_string(3, device_uuid)
        + field_string(4, field_varint(1, channel))
    )

plant_id = b"dfe0b3ee-49b7-4969-ac64-5ee1174a5675"
dev_uuid = b"bfcd8bfd-d698-457a-9345-4cb38028a98f"
body = build_switch_body(plant_id, dev_uuid, 1)
print("gRPC payload body (hex):", body.hex())
