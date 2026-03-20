import pytest
from lgbfscotland.lgbfscotland import app_ui, server
from htmltools import Tag


def test_app_ui():
    assert isinstance(app_ui, Tag)
