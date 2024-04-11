from typing import Annotated

import typer

from .commands.copy import copy_command
from .commands.init import init_command
from .commands.list import list_command
from .commands.play import play_command
from .commands.tag import tag_command
from rolabesti import __app_name__, __description__, __version__


app = typer.Typer()
app.command("copy")(copy_command)
app.command("init")(init_command)
app.command("list")(list_command)
app.command("play")(play_command)
app.command("tag")(tag_command)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} version: {__version__}")
        raise typer.Exit()


@app.callback(help=__description__)
def callback(
    version: Annotated[bool, typer.Option(
        "--version",
        help="Show the application version and exit.",
        callback=version_callback,
    )] = False,
) -> None:
    return
