import typer


def validate_length_limits(
    max_track_length: int,
    min_track_length: int,
    max_tracklist_length: int | None = None,
) -> None:
    """
    Ensure both conditions:
        -min_track_length < max_track_length, unless max_track_length is zero
        -max_track_length <= max_tracklist_length, unless max_tracklist_length is zero or None
    """
    if max_track_length and not (min_track_length < max_track_length):
        raise typer.BadParameter("maximum track length should be greater than minimum track length.")
    if max_tracklist_length and not (max_track_length <= max_tracklist_length):
        raise typer.BadParameter("maximum tracklist length should be greater than or equal to maximum track length.")
