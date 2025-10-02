from commizard.utils.terminal import clear_screen

def test_clear_screen_does_not_raise(capsys):
    clear_screen()
    out, err = capsys.readouterr()
    assert err == ""
