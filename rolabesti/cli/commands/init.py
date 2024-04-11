from pathlib import Path
from typing import Annotated

import typer

from rolabesti.conf.settings import MUSIC_DIR
from rolabesti.mongo import load


app = typer.Typer()
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
def init_command(
    music_directory: music_directory_option = MUSIC_DIR,
):
    """Initialize database."""
    load(music_directory)
