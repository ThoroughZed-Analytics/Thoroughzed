import pytest
from app.main import run_cli


def test_cli_quit(monkeypatch):
    with pytest.raises(SystemExit) as e:
        monkeypatch.setattr('builtins.input', lambda _:'q')
        run_cli()
    assert e.type == SystemExit
