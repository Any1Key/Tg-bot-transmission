# Copyright (c) 2026 Any1Key
SPECIAL = r"_*[]()~`>#+-=|{}.!"


def esc(text: str) -> str:
    out = text
    for ch in SPECIAL:
        out = out.replace(ch, f"\\{ch}")
    return out
