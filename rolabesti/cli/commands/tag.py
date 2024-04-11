from enum import Enum
from typing import Annotated

import typer

from ..options import (
    max_track_length_option,
    min_track_length_option,
    artist_option,
    title_option,
    album_option,
    genre_option,
    place_option,
)
from ..utils import get_search_arguments, validate_length_limits
from rolabesti.conf.settings import MAX_TRACK_LENGTH, MIN_TRACK_LENGTH
from rolabesti.mongo import search
from rolabesti.tagger import tag


class ID3TagEnum(str, Enum):
    artist = "artist"
    title = "title"
    album = "album"
    genre = "genre"


app = typer.Typer()
id3_tag_option = Annotated[ID3TagEnum, typer.Option(
    "--id3-tag",
    help="ID3 tag to be updated.",
    show_default=False,
)]


@app.command()
def tag_command(
    id3_tag: id3_tag_option,
    max_track_length: max_track_length_option = MAX_TRACK_LENGTH,
    min_track_length: min_track_length_option = MIN_TRACK_LENGTH,
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
):
    """Update ID3 tags with path fields."""
    validate_length_limits(max_track_length, min_track_length)
    search_arguments = get_search_arguments(locals())
    tracks, length = search(search_arguments)
    tag(tracks, id3_tag)
