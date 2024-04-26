import typer

from ..options import (
    artist_option,
    title_option,
    album_option,
    genre_option,
    place_option,
    max_track_length_option,
    min_track_length_option,
    sorting_option,
)
from ..utils import validate_length_limits
from rolabesti.conf.settings import MAX_TRACK_LENGTH, MIN_TRACK_LENGTH, SORTING
from rolabesti.controllers import ListController
from rolabesti.models import Sortings


app = typer.Typer()


@app.command()
def list_(
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
    max_track_length: max_track_length_option = MAX_TRACK_LENGTH,
    min_track_length: min_track_length_option = MIN_TRACK_LENGTH,
    sorting: sorting_option = Sortings[SORTING],
):
    """List matching tracks."""
    validate_length_limits(max_track_length, min_track_length)
    ListController(locals())()
