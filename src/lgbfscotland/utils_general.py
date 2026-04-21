import re
import textwrap


def clean_id(x: str) -> str:
    x = x.lower().strip()
    x = re.sub(r"[\s\-]+", "_", x)
    x = re.sub(r"[^\w]+", "", x)
    return x.strip("_")


def wrap_text(x: str, width: float = 40):
    return "<br>".join(textwrap.wrap(x, width=width))
