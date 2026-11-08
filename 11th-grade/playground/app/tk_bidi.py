"""
Tkinter on Windows often ignores the Unicode bidi algorithm.
Keep Persian and Latin on separate widgets when possible; otherwise embed RLE/PDF.
"""

from __future__ import annotations

# Right-to-Left Embedding … Pop Directional Formatting
_RLE = "\u202B"
_PDF = "\u202C"
_LRE = "\u202A"


def rtl(text: str) -> str:
    """Force a Persian (or other RTL) run to render right-to-left in Tk labels."""
    s = "" if text is None else str(text)
    if not s:
        return s
    # Strip previous embeddings so we do not nest forever on refresh.
    s = s.replace(_RLE, "").replace(_PDF, "").replace(_LRE, "")
    return f"{_RLE}{s}{_PDF}"


def ltr(text: str) -> str:
    """Force a Latin/URL/path run to stay left-to-right inside Tk."""
    s = "" if text is None else str(text)
    if not s:
        return s
    s = s.replace(_RLE, "").replace(_PDF, "").replace(_LRE, "")
    return f"{_LRE}{s}{_PDF}"
