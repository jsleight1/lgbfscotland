import re
import textwrap


def clean_id(x: str):
    x = x.lower().strip()
    x = re.sub(r"[\s\-]+", "_", x)
    x = re.sub(r"[^\w]+", "", x)
    return x.strip("_")


def wrap_text(x):
    return "<br>".join(textwrap.wrap(x, width=40))
