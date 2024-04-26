from enum import Enum
from typing import Annotated, Optional

import typer

from rolabesti.models import Sortings


def enum_callback(enum: Enum):
    """Return enum's value."""
    return enum.value


def field_callback(field: str | None):
    """Ensure non-empty string."""
    if field == "":
        raise typer.BadParameter("should not be empty.")
    return field


def length_callback(length: int):
    """Convert minutes to seconds."""
    return length * 60


artist_option = Annotated[Optional[str], typer.Option(
    "--artist",
    "-ar",
    help="Track artist.",
    rich_help_panel="Search filters",
    show_default=False,
    callback=field_callback,
)]
title_option = Annotated[Optional[str], typer.Option(
    "--title",
    "-t",
    help="Track title.",
    rich_help_panel="Search filters",
    show_default=False,
    callback=field_callback,
)]
album_option = Annotated[Optional[str], typer.Option(
    "--album",
    "-al",
    help="Track album.",
    rich_help_panel="Search filters",
    show_default=False,
    callback=field_callback,
)]
genre_option = Annotated[Optional[str], typer.Option(
    "--genre",
    "-g",
    help="Track genre.",
    rich_help_panel="Search filters",
    show_default=False,
    callback=field_callback,
)]
place_option = Annotated[Optional[str], typer.Option(
    "--place",
    "-p",
    help="Track place.",
    rich_help_panel="Search filters",
    show_default=False,
    callback=field_callback,
)]
max_track_length_option = Annotated[int, typer.Option(
    "--max",
    help="Maximum track length in minutes (0 means disabled).",
    rich_help_panel="Search filters",
    min=0,
    callback=length_callback,
)]
min_track_length_option = Annotated[int, typer.Option(
    "--min",
    help="Minimum track length in minutes.",
    rich_help_panel="Search filters",
    min=0,
    callback=length_callback,
)]
max_tracklist_length_option = Annotated[int, typer.Option(
    "--length",
    "-l",
    help="Maximum tracklist length in minutes (0 means disabled).",
    rich_help_panel="Tracklist selectors",
    min=0,
    callback=length_callback,
)]
sorting_option = Annotated[Sortings, typer.Option(
    "--sorting",
    "-s",
    help="Order by track path.",
    rich_help_panel="Tracklist selectors",
    callback=enum_callback,
)]
