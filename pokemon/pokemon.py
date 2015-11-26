from contextlib import contextmanager
from functools import partial
import os


def play_sound(path):
    pid = os.fork()
    if pid == 0:
        os.execl('/usr/bin/afplay', 'afplay', path)
    else:
        return pid


play_battle = partial(play_sound, 'battle.mp3')
play_success = partial(play_sound, 'success.m4a')


@contextmanager
def pokemon_music():
    """
    Context manager that plays the pokemon battle music during a long task.
    When the task is finished, the success catch music is played.

    Example:
        import time
        from pokemon import pokemon_music

        with pokemon_music():
            time.sleep(10)
            print("Success !")
    """
    pid = play_battle()
    yield
    os.kill(pid, 9)
    play_success()
