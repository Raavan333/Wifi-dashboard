import re


MAC_ADDRESS_REGEX = re.compile(
    r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
)


def is_valid_mac(
    mac: str,
) -> bool:

    if not mac:
        return False

    return bool(
        MAC_ADDRESS_REGEX.match(mac)
    )