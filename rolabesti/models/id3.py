from enum import Enum


class ID3Tags(str, Enum):
    artist = "artist"
    title = "title"
    album = "album"
    genre = "genre"
