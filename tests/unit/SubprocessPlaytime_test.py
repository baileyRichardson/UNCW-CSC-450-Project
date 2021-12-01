import pytest

import SubprocessPlaytime


def test_update():
    assert (SubprocessPlaytime.update_playtime("aan7056@uncwedu") == True)
