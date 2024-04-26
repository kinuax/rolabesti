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
    max_tracklist_length_option,
    sorting_option,
)
from ..utils import validate_length_limits
from rolabesti.conf.settings import (
    MAX_TRACK_LENGTH,
    MIN_TRACK_LENGTH,
    MAX_TRACKLIST_LENGTH,
    SORTING,
    OVERLAP_LENGTH,
)
from rolabesti.controllers import PlayController
from rolabesti.models import Sortings


app = typer.Typer()
cli_option = Annotated[bool, typer.Option(
    help="Select cli or default app.",
)]
overlap_length_option = Annotated[int, typer.Option(
    "--overlap-length",
    "-o",
    help="Overlap length in seconds between two consecutive tracks (only with --cli).",
    min=0,
    max=30,
)]


@app.command()
def play(
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
    max_track_length: max_track_length_option = MAX_TRACK_LENGTH,
    min_track_length: min_track_length_option = MIN_TRACK_LENGTH,
    max_tracklist_length: max_tracklist_length_option = MAX_TRACKLIST_LENGTH,
    sorting: sorting_option = Sortings[SORTING],
    cli: cli_option = True,
    overlap_length: overlap_length_option = OVERLAP_LENGTH,
):
    """Play and enqueue matching tracks."""
    validate_length_limits(max_track_length, min_track_length, max_tracklist_length)
    PlayController(locals())()
