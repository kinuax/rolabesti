import typer

from rolabesti.cli.options import (
    artist_option,
    title_option,
    album_option,
    genre_option,
    place_option,
    max_track_length_option,
    min_track_length_option,
    sorting_option,
)
from rolabesti.cli.utils import validate_length_limits
from rolabesti.config import get_settings
from rolabesti.controllers import ListController


app = typer.Typer()
settings = get_settings()


@app.command()
def list_(
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
    max_track_length: max_track_length_option = settings.max_track_length,
    min_track_length: min_track_length_option = settings.min_track_length,
    sorting: sorting_option = settings.sorting,
):
    """List matching tracks."""
    validate_length_limits(max_track_length, min_track_length)
    ListController(locals())()
