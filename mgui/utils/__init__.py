# mgui utils package
try:
    import bmfont
    __all__ = [
        "bmfont",
    ]
except Exception as e:
    from . import bmfont
    __all__ = [
        "bmfont",
    ]

