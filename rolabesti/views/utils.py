import contextlib
from pathlib import Path
from wurlitzer import pipes

# Avoid messages from pygame while importing.
with contextlib.redirect_stdout(None):
    import pygame


def play_audio(trackpath: Path) -> None:
    """Play the audio file located at trackpath."""
    pygame.mixer.init()
    # Avoid messages from C libraries.
    with pipes():
        pygame.mixer.music.load(trackpath)
    pygame.mixer.music.play()
