from enum import Enum
from typing import Annotated

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
    max_tracklist_length_option,
    sorting_option,
)
from ..utils import get_search_arguments, validate_length_limits
from rolabesti.conf.settings import (
    MAX_TRACK_LENGTH,
    MIN_TRACK_LENGTH,
    MAX_TRACKLIST_LENGTH,
    SORTING,
    PLAYER,
    OVERLAP_LENGTH,
)
from rolabesti.displayer import display
from rolabesti.mongo import search
from rolabesti.player import play
from rolabesti.slicer import slice_tracks
from rolabesti.sorter import sort


class PlayerEnum(str, Enum):
    shell = "shell"
    vlc = "vlc"


app = typer.Typer()
player_option = Annotated[PlayerEnum, typer.Option(
    "--player",
    help="Player.",
)]
overlap_length_option = Annotated[int, typer.Option(
    "--overlap-length",
    "-o",
    help="With shell player, overlap length in seconds between two consecutive tracks.",
    min=0,
    max=30,
)]


@app.command()
def play_command(
    max_track_length: max_track_length_option = MAX_TRACK_LENGTH,
    min_track_length: min_track_length_option = MIN_TRACK_LENGTH,
    artist: artist_option = None,
    title: title_option = None,
    album: album_option = None,
    genre: genre_option = None,
    place: place_option = None,
    max_tracklist_length: max_tracklist_length_option = MAX_TRACKLIST_LENGTH,
    sorting: sorting_option = SortingEnum[SORTING],
    player: player_option = PlayerEnum[PLAYER],
    overlap_length: overlap_length_option = OVERLAP_LENGTH,
):
    """Play and enqueue matching tracks."""
    validate_length_limits(max_track_length, min_track_length, max_tracklist_length)
    search_arguments = get_search_arguments(locals())
    tracks, length = search(search_arguments)
    tracks = sort(tracks, sorting.value)

    if max_tracklist_length:
        tracks, length = slice_tracks(tracks, max_tracklist_length)

    display(tracks, length)
    play(tracks, player.value, overlap_length)
