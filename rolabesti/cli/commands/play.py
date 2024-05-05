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
from rolabesti.config import get_settings, max_overlap_length
from rolabesti.controllers import PlayController


app = typer.Typer()
settings = get_settings()
cli_option = Annotated[bool, typer.Option(
    help="Select cli or default app.",
)]
overlap_length_option = Annotated[int, typer.Option(
    "--overlap-length",
    "-o",
    help="Overlap length in seconds between two consecutive tracks (only with --cli, 0 means disabled).",
    min=0,
    max=max_overlap_length,
)]


@app.command()
def play(
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
    max_track_length: max_track_length_option = settings.max_track_length,
    min_track_length: min_track_length_option = settings.min_track_length,
    max_tracklist_length: max_tracklist_length_option = settings.max_tracklist_length,
    sorting: sorting_option = settings.sorting,
    cli: cli_option = True,
    overlap_length: overlap_length_option = settings.overlap_length,
):
    """Play and enqueue matching tracks."""
    validate_length_limits(max_track_length, min_track_length, max_tracklist_length)
    PlayController(locals())()
