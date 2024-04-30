import re
from pathlib import Path

from mutagen import MutagenError
from mutagen.mp3 import MP3
from pydantic import ValidationError

from .utils import add_prefix_to_dict, get_id3_dict
from rolabesti.models import ID3Tags, Track


PATTERNS = {
    r"/Places/([^/]+)/Genres/([^/]+)/Albums/([^/]+)/(?:([^/]+)/)?([^/]+)\.[mM][pP]3$": (
        "place", "genre", "album", "side", "title"),
    r"/Places/([^/]+)/Genres/([^/]+)/([^/]+)/([^/]+)/(?:([^/]+)/)?([^/]+)\.[mM][pP]3$": (
        "place", "genre", "artist", "album", "side", "title"),
    r"/Places/([^/]+)/Genres/([^/]+)/([^/]+)/([^/]+)\.[mM][pP]3$": ("place", "genre", "artist", "title"),
    r"/Places/([^/]+)/Genres/([^/]+)/([^/]+)\.[mM][pP]3$": ("place", "genre", "title"),
    r"/Places/([^/]+)/([^/]+)\.[mM][pP]3$": ("place", "title"),
    r"/Places/([^/]+)/Albums/([^/]+)/(?:([^/]+)/)?([^/]+)\.[mM][pP]3$": ("place", "album", "side", "title"),
    r"/Places/([^/]+)/([^/]+)/([^/]+)/(?:([^/]+)/)?([^/]+)\.[mM][pP]3$": ("place", "artist", "album", "side", "title"),
    r"/Places/([^/]+)/([^/]+)/([^/]+)\.[mM][pP]3$": ("place", "artist", "title"),
    r"/Genres/([^/]+)/Albums/([^/]+)/(?:([^/]+)/)?([^/]+)\.[mM][pP]3$": ("genre", "album", "side", "title"),
    r"/Genres/([^/]+)/([^/]+)/([^/]+)/(?:([^/]+)/)?([^/]+)\.[mM][pP]3$": ("genre", "artist", "album", "side", "title"),
    r"/Genres/([^/]+)/([^/]+)/([^/]+)\.[mM][pP]3$": ("genre", "artist", "title"),
    r"/Genres/([^/]+)/([^/]+)\.[mM][pP]3$": ("genre", "title"),
    r"/Artists/([^/]+)/([^/]+)/(?:([^/]+)/)?([^/]+)\.[mM][pP]3$": ("artist", "album", "side", "title"),
    r"/Artists/([^/]+)/([^/]+)\.[mM][pP]3$": ("artist", "title"),
    r"/Albums/([^/]+)/(?:([^/]+)/)?([^/]+)\.[mM][pP]3$": ("album", "side", "title"),
    r"/([^/]+)\.[mM][pP]3$": ("title",),
}


class Parser:
    """Parsing related functionality."""
    def parse(self, trackpath: Path) -> Track | None:
        """
        Parse track located at trackpath and return a Track object.
        If there is an error, return None.
        """
        if (path_fields := self._parse_path_fields(trackpath)) is None:
            return
        if (id3_tags := self._parse_id3_tags(trackpath)) is None:
            return
        if (length := self._parse_length(trackpath)) is None:
            return
        if (track := self._build_track(trackpath, path_fields, id3_tags, length)) is None:
            return
        return track

    @staticmethod
    def _parse_path_fields(trackpath: Path) -> dict | None:
        """
        Match and parse trackpath against PATTERNS.
        Return a dictionary with parsed fields if there is a match.
        If there is no matching pattern, return None.
        """
        for regex, fields in PATTERNS.items():
            match = re.search(regex, str(trackpath))
            if match:
                return {field: value for field, value in zip(fields, match.groups()) if value}

    @staticmethod
    def _parse_id3_tags(trackpath: Path) -> dict | None:
        """
        Return a dictionary with the ID3 tags of the track located at trackpath.
        The tags are limited to ID3Tags. If there is no tag to retrieve, return an empty dictionary.
        If there is an error retrieving the ID3 tags, return None.
        """
        if (id3_dict := get_id3_dict(trackpath)) is None:
            return
        id3_tags = {}
        for id3_tag in set.intersection({id3_tag.value for id3_tag in ID3Tags},
                                        {id3_tag for id3_tag, id3_value in id3_dict.items() if id3_value}):
            # Avoid parsing empty tags.
            if value := id3_dict[id3_tag][0].strip():
                id3_tags[id3_tag] = value
        return id3_tags

    @staticmethod
    def _parse_length(trackpath: Path) -> int | None:
        """
        Return the length of the track located at trackpath in seconds.
        If there is an error retrieving the length, return None.
        """
        try:
            return int(MP3(trackpath).info.length)
        except MutagenError:
            return

    @staticmethod
    def _build_track(trackpath: Path, path_fields: dict, id3_tags: dict, length: int) -> Track | None:
        """
        Build and return a Track object.
        If there is a validation error, return None.
        """
        track = {"path": trackpath, "length": length}
        track.update(add_prefix_to_dict(path_fields, "path"))
        track.update(add_prefix_to_dict(id3_tags, "id3"))
        try:
            return Track(**track)
        except ValidationError:
            return
