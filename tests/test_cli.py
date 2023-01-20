import pytest
from app.thoroughzed_cli import run_cli
from app.meta_data_query_and_loop_script import get_summary_horse_data
from io import StringIO


def test_cli_quit(monkeypatch):
    with pytest.raises(SystemExit) as e:
        monkeypatch.setattr('builtins.input', lambda _:'q')
        run_cli()
    assert e.type == SystemExit

# def test_cli_help(monkeypatch,capfd):
#     with pytest.raises(SystemExit) as e:
#         monkeypatch.setattr('builtins.input', lambda _: '1000')
#         run_cli()
#         out,err = capfd.readouterr()
#     assert out == "Would you like to find the (r)elative value or (i)ntrinsic value? Or type 'q' to quit. Or h for help"
