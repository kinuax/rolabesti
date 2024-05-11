from pathlib import Path
from typing import Annotated

import typer

from rolabesti.cli.options import (
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
from rolabesti.cli.utils import validate_length_limits
from rolabesti.config import get_settings
from rolabesti.controllers import CopyController


app = typer.Typer()
settings = get_settings()
copy_directory_option = Annotated[Path, typer.Option(
    "--copy-directory",
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
    max_track_length: max_track_length_option = settings.max_track_length,
    min_track_length: min_track_length_option = settings.min_track_length,
    max_tracklist_length: max_tracklist_length_option = settings.max_tracklist_length,
    sorting: sorting_option = settings.sorting,
    copy_directory: copy_directory_option = settings.copy_directory,
):
    """Copy matching tracks to a directory."""
    validate_length_limits(max_track_length, min_track_length, max_tracklist_length)
    CopyController(locals())()
