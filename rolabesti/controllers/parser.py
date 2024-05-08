from pathlib import Path

from mutagen import MutagenError
from mutagen.mp3 import MP3
from pydantic import ValidationError

from .utils import add_prefix_to_dict, get_id3_dict
from rolabesti.models import ID3Tags, Track


patterns = [
    [{"Places": -8, "Genres": -6, "Albums": -4}, {"place": -7, "genre": -5, "album": -3}],
    [{"Places": -7, "Genres": -5, "Albums": -3}, {"place": -6, "genre": -4, "album": -2}],
    [{"Places": -8, "Genres": -6}, {"place": -7, "genre": -5, "artist": -4, "album": -3}],
    [{"Places": -7, "Genres": -5}, {"place": -6, "genre": -4, "artist": -3, "album": -2}],
    [{"Places": -6, "Genres": -4}, {"place": -5, "genre": -3, "artist": -2}],
    [{"Places": -5, "Genres": -3}, {"place": -4, "genre": -2}],
    [{"Places": -6, "Albums": -4}, {"place": -5, "album": -3}],
    [{"Places": -5, "Albums": -3}, {"place": -4, "album": -2}],
    [{"Places": -6}, {"place": -5, "artist": -4, "album": -3}],
    [{"Places": -5}, {"place": -4, "artist": -3, "album": -2}],
    [{"Places": -4}, {"place": -3, "artist": -2}],
    [{"Places": -3}, {"place": -2}],
    [{"Genres": -6, "Albums": -4}, {"genre": -5, "album": -3}],
    [{"Genres": -5, "Albums": -3}, {"genre": -4, "album": -2}],
    [{"Genres": -6}, {"genre": -5, "artist": -4, "album": -3}],
    [{"Genres": -5}, {"genre": -4, "artist": -3, "album": -2}],
    [{"Genres": -4}, {"genre": -3, "artist": -2}],
    [{"Genres": -3}, {"genre": -2}],
    [{"Artists": -5}, {"artist": -4, "album": -3}],
    [{"Artists": -4}, {"artist": -3, "album": -2}],
    [{"Artists": -3}, {"artist": -2}],
    [{"Albums": -4}, {"album": -3}],
    [{"Albums": -3}, {"album": -2}],
]


class Parser:
    """Parsing related functionality."""

    def parse(self, trackpath: Path) -> Track | None:
        """
        Parse track located at trackpath and return a Track object.
        If there is an error, return None.
        """
        if (id3_tags := self._parse_id3_tags(trackpath)) is None:
            return
        if (length := self._parse_length(trackpath)) is None:
            return
        path_fields = self._parse_path_fields(trackpath)
        path_fields["title"] = trackpath.stem
        if (track := self._build_track(trackpath, path_fields, id3_tags, length)) is None:
            return
        return track

    @staticmethod
    def _parse_path_fields(trackpath: Path) -> dict:
        """
        Parse trackpath and return a dictionary with the path fields.
        If there is no matching pattern, return an empty dictionary.
        """
        for pattern in patterns:
            try:
                if all(field == trackpath.parts[index] for field, index in pattern[0].items()):
                    return {field: trackpath.parts[index] for field, index in pattern[1].items()}
            except IndexError:
                # Discard trackpath unable to match pattern.
                pass
        return {}

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
