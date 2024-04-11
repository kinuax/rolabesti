from enum import Enum
from typing import Annotated

import typer


class SortingEnum(str, Enum):
    asc = "asc"
    desc = "desc"
    random = "random"


def length_callback(length: int):
    """Convert minutes to seconds."""
    return length * 60


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
artist_option = Annotated[str, typer.Option(
    "--artist",
    "-ar",
    help="Track artist.",
    rich_help_panel="Search filters",
    show_default=False,
)]
title_option = Annotated[str, typer.Option(
    "--title",
    "-t",
    help="Track title.",
    rich_help_panel="Search filters",
    show_default=False,
)]
album_option = Annotated[str, typer.Option(
    "--album",
    "-al",
    help="Track album.",
    rich_help_panel="Search filters",
    show_default=False,
)]
genre_option = Annotated[str, typer.Option(
    "--genre",
    "-g",
    help="Track genre.",
    rich_help_panel="Search filters",
    show_default=False,
)]
place_option = Annotated[str, typer.Option(
    "--place",
    "-p",
    help="Track place.",
    rich_help_panel="Search filters",
    show_default=False,
)]
max_tracklist_length_option = Annotated[int, typer.Option(
    "--length",
    "-l",
    help="Maximum tracklist length in minutes (0 means disabled).",
    rich_help_panel="Tracklist selectors",
    min=0,
    callback=length_callback,
)]
sorting_option = Annotated[SortingEnum, typer.Option(
    "--sorting",
    "-s",
    help="Order by track path.",
    rich_help_panel="Tracklist selectors",
)]
