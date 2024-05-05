from typing import Annotated

import typer

from ..options import (
    artist_option,
    title_option,
    album_option,
    genre_option,
    place_option,
    max_track_length_option,
    min_track_length_option,
    enum_callback,
)
from ..utils import validate_length_limits
from rolabesti.config import get_settings
from rolabesti.controllers import TagController
from rolabesti.models import ID3Tags


app = typer.Typer()
settings = get_settings()
id3_tag_option = Annotated[ID3Tags, typer.Option(
    "--id3-tag",
    help="ID3 tag to be updated.",
    show_default=False,
    callback=enum_callback,
)]


@app.command()
def tag(
    id3_tag: id3_tag_option,
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
    max_track_length: max_track_length_option = settings.max_track_length,
    min_track_length: min_track_length_option = settings.min_track_length,
):
    """Update ID3 tags with path fields (file and database)."""
    validate_length_limits(max_track_length, min_track_length)
    TagController(locals())()
