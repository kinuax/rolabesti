from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError


def add_prefix_to_dict(d: dict, prefix: str) -> dict:
    """Return a dictionary with keys prefixed by prefix_."""
    return {f"{prefix}_{key}": value for key, value in d.items()}


def get_id3_dict(trackpath: Path) -> EasyID3 | None:
    """
    Return an instance of EasyID3 (dictionary-like object) corresponding to the track located at trackpath.
    If there is an error, return None.
    """
    try:
        return EasyID3(trackpath)
    except ID3NoHeaderError:
        return
