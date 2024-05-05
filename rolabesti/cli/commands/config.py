from pathlib import Path
from typing import Annotated

import typer

from ..utils import validate_length_limits
from rolabesti.config import get_settings, max_overlap_length
from rolabesti.controllers import ConfigController
from rolabesti.models import Sortings


app = typer.Typer()
settings = get_settings()
list_option = Annotated[bool, typer.Option(
    "--list",
    help="List configuration settings.",
)]
reset_option = Annotated[bool, typer.Option(
    "--reset",
    help="Reset configuration settings.",
)]
max_track_length_option = Annotated[int, typer.Option(
    "--max",
    help="Set default maximum track length in minutes (0 means disabled).",
    rich_help_panel="Main settings",
    show_default=False,
    min=0,
)]
min_track_length_option = Annotated[int, typer.Option(
    "--min",
    help="Set default minimum track length in minutes.",
    rich_help_panel="Main settings",
    show_default=False,
    min=0,
)]
max_tracklist_length_option = Annotated[int, typer.Option(
    "--length",
    "-l",
    help="Set default maximum tracklist length in minutes (0 means disabled).",
    rich_help_panel="Main settings",
    show_default=False,
    min=0,
)]
sorting_option = Annotated[Sortings, typer.Option(
    "--sorting",
    "-s",
    help="Set default order by track path.",
    rich_help_panel="Main settings",
    show_default=False,
)]
overlap_length_option = Annotated[int, typer.Option(
    "--overlap-length",
    "-o",
    help="Set default overlap length in seconds between two consecutive tracks (0 means disabled).",
    rich_help_panel="Play settings",
    show_default=False,
    min=0,
    max=max_overlap_length,
)]
music_directory_option = Annotated[Path, typer.Option(
    "--music-directory",
    help="Set default path to mp3 files.",
    rich_help_panel="Database settings",
    show_default=False,
    exists=True,
    file_okay=False,
    dir_okay=True,
    readable=True,
    resolve_path=True,
)]
copy_directory_option = Annotated[Path, typer.Option(
    "--copy-directory",
    help="Set default path to destiny directory.",
    rich_help_panel="Copy settings",
    show_default=False,
    exists=True,
    file_okay=False,
    dir_okay=True,
    writable=True,
    resolve_path=True,
)]


@app.command()
def config(
    list_: list_option = False,
    reset: reset_option = False,
    max_track_length: max_track_length_option = None,
    min_track_length: min_track_length_option = None,
    max_tracklist_length: max_tracklist_length_option = None,
    sorting: sorting_option = None,
    overlap_length: overlap_length_option = None,
    music_directory: music_directory_option = None,
    copy_directory: copy_directory_option = None,
):
    """Manage configuration settings."""
    validate_length_limits(
        max_track_length if max_track_length is not None else settings.max_track_length,
        min_track_length if min_track_length is not None else settings.min_track_length,
        max_tracklist_length if max_tracklist_length is not None else settings.max_tracklist_length,
    )
    ConfigController(locals())()
