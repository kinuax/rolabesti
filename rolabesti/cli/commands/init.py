from pathlib import Path
from typing import Annotated

import typer

from rolabesti.config import get_settings
from rolabesti.controllers import InitController


app = typer.Typer()
settings = get_settings()
music_directory_option = Annotated[Path, typer.Option(
    "--music-directory",
    "-d",
    help="Path to mp3 files.",
    exists=True,
    file_okay=False,
    dir_okay=True,
    readable=True,
    resolve_path=True,
)]


@app.command()
def init(
    music_directory: music_directory_option = settings.music_directory,
):
    """Initialize database."""
    InitController(locals())()
