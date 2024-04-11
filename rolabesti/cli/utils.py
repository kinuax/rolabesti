import typer

SEARCH_ARGUMENTS = {"max_track_length", "min_track_length", "artist", "title", "album", "genre", "place"}

def get_search_arguments(options: dict) -> dict:
    """Convert CLI options to search arguments."""
    arguments = {}

    for option, value in options.items():
        if value is not None and option in SEARCH_ARGUMENTS:
            arguments[option] = value

    return arguments


def validate_length_limits(
    max_track_length: int,
    min_track_length: int,
    max_tracklist_length: int | None = None,
) -> None:
    """
    Ensure both conditions:
        -min_track_length < max_track_length
        -max_track_length <= max_tracklist_length, unless max_tracklist_length is zero or undefined
    """
    if not (min_track_length < max_track_length):
        raise typer.BadParameter("Maximum track length should be greater than minimum track length.")
    if max_tracklist_length and not (max_track_length <= max_tracklist_length):
        raise typer.BadParameter("Maximum tracklist length should be greater than or equal to minimum track length.")
