# Copyright (c) 2026 Any1Key

def human(n: int) -> str:
    units=["B","KB","MB","GB","TB"]
    v=float(n); i=0
    while v>=1024 and i<len(units)-1:
        v/=1024; i+=1
    return f"{v:.2f} {units[i]}"
