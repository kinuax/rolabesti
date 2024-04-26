from typing import Annotated

import typer
from click import Context
from typer.core import TyperGroup

from .commands.copy import copy
from .commands.init import init
from .commands.list import list_
from .commands.play import play
from .commands.tag import tag
from rolabesti import __app_name__, __description__, __version__


class OrderCommandsTyperGroup(TyperGroup):
    def list_commands(self, ctx: Context):
        return list(self.commands)


app = typer.Typer(
    cls=OrderCommandsTyperGroup,
    context_settings={"help_option_names": ["-h", "--help"]},
)
app.command()(init)
app.command("list")(list_)
app.command()(play)
app.command()(copy)
app.command()(tag)


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
    pass
