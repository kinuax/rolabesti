from pathlib import Path
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
from rolabesti.conf.settings import MAX_TRACK_LENGTH, MIN_TRACK_LENGTH, MAX_TRACKLIST_LENGTH, SORTING, COPY_DIR
from rolabesti.controllers import CopyController
from rolabesti.models import Sortings


app = typer.Typer()
directory_option = Annotated[Path, typer.Option(
    "--directory",
    "-d",
    help="Path to destiny directory.",
    exists=True,
    file_okay=False,
    dir_okay=True,
    writable=True,
    resolve_path=True,
)]


@app.command()
def copy(
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
    max_track_length: max_track_length_option = MAX_TRACK_LENGTH,
    min_track_length: min_track_length_option = MIN_TRACK_LENGTH,
    max_tracklist_length: max_tracklist_length_option = MAX_TRACKLIST_LENGTH,
    sorting: sorting_option = Sortings[SORTING],
    directory: directory_option = COPY_DIR,
):
    """Copy matching tracks to a directory."""
    validate_length_limits(max_track_length, min_track_length, max_tracklist_length)
    CopyController(locals())()
