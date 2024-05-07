from contextlib import contextmanager, redirect_stdout
from pathlib import Path

try:
    from wurlitzer import pipes
except ModuleNotFoundError:
    # wurlitzer is not supported on Windows.
    @contextmanager
    def pipes():
        yield


# Avoid messages from pygame while importing.
with redirect_stdout(None):
    import pygame


def play_audio(trackpath: Path) -> None:
    """Play the audio file located at trackpath."""
    pygame.mixer.init()
    # Avoid messages from C libraries.
    with pipes():
        pygame.mixer.music.load(trackpath)
    pygame.mixer.music.play()
