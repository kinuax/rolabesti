import tempfile
from contextlib import contextmanager, redirect_stdout
from pathlib import Path

from pydub import AudioSegment


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


pygame.mixer.init()
channels = [pygame.mixer.Channel(0), pygame.mixer.Channel(1)]


def play_mp3(trackpath: Path, channel: int) -> None:
    """Play the track located at trackpath on the given channel."""
    # Avoid messages from C libraries.
    with pipes():
        try:
            sound = pygame.mixer.Sound(trackpath)
        except pygame.error:
            # Convert mp3 to wav if "Unrecognized audio format" error.
            with tempfile.TemporaryFile() as wav_file:
                AudioSegment.from_mp3(trackpath).export(wav_file, format="wav")
                sound = pygame.mixer.Sound(wav_file)
        channels[channel].play(sound)
