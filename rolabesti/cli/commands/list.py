import typer

from ..options import (
    SortingEnum,
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
from rolabesti.displayer import display
from rolabesti.mongo import search
from rolabesti.sorter import sort

app = typer.Typer()


@app.command()
def list_command(
    max_track_length: max_track_length_option = MAX_TRACK_LENGTH,
    min_track_length: min_track_length_option = MIN_TRACK_LENGTH,
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
):
    """List matching tracks."""
    validate_length_limits(max_track_length, min_track_length)
    search_arguments = get_search_arguments(locals())
    tracks, length = search(search_arguments)
    tracks = sort(tracks, SortingEnum["asc"])
    display(tracks, length)
