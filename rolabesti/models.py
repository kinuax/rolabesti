from enum import Enum

from pydantic import BaseModel, FilePath, NonNegativeInt, field_serializer


FIELD_FILTERS = {
    "artist": ("path_artist", "id3_artist"),
    "title": ("path_title", "id3_title"),
    "album": ("path_album", "id3_album"),
    "genre": ("path_genre", "id3_genre"),
    "place": ("path_place",),
}
LENGTH_FILTERS = {"max_track_length", "min_track_length"}
SEARCH_FILTERS = set.union(set(FIELD_FILTERS), LENGTH_FILTERS)


class ID3Tags(str, Enum):
    artist = "artist"
    title = "title"
    album = "album"
    genre = "genre"


class Sortings(str, Enum):
    asc = "asc"
    desc = "desc"
    random = "random"


class Players(str, Enum):
    shell = "shell"
    vlc = "vlc"


class Track(BaseModel):
    path: FilePath
    length: NonNegativeInt
    id3_artist: str | None = None
    id3_title: str | None = None
    id3_album: str | None = None
    id3_genre: str | None = None
    path_artist: str | None = None
    path_title: str | None = None
    path_album: str | None = None
    path_genre: str | None = None
    path_place: str | None = None

    @field_serializer("path")
    def serialize_path(self, path: FilePath, _info):
        return str(path)
