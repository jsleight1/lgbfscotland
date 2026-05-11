import pytest
from lgbfscotland.utils_general import clean_id, wrap_text


def test_clean_id():
    assert (
        clean_id("asdf -asdfln *asdflk/sf\a//235&$£*bn") == "asdf_asdfln_asdflksf235bn"
    )


def test_wrap_text():
    assert wrap_text("text") == "text"
    assert wrap_text("text", width=2) == "te<br>xt"
