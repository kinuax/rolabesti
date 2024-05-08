from pathlib import Path

import typer
from pydantic import ValidationError

from .controller import Controller

from rolabesti.config import get_settings, reset_settings, store_settings


class ConfigController(Controller):
    def __call__(self) -> None:
        """List, reset, and set settings."""
        if self.parameters["list_"]:
            settings = get_settings()
            self.logger.log("[italic green]--------------- SETTINGS ---------------[/italic green]")
            for setting, value in settings.model_dump().items():
                self.logger.log(f"[bold blue]{setting}[/bold blue] = [bold green]{value}[/bold green]")
            self.logger.log("[italic green]----------------------------------------[/italic green]")
        elif self.parameters["reset"]:
            reset_settings()
            self.logger.log("[green]settings are reset[/green]")
        else:
            del self.parameters["list_"]
            del self.parameters["reset"]

            if all(parameter is None for parameter in self.parameters.values()):
                self.logger.log("[green]no new settings to configure[/green]")
                return

            settings = get_settings()
            for parameter, value in self.parameters.items():
                if value is not None:
                    if isinstance(value, Path):
                        value = str(value)
                    try:
                        setattr(settings, parameter, value)
                    except ValidationError as error:
                        raise typer.BadParameter(f"{parameter} - {error.errors()[0]['msg']}.")

            store_settings(settings)
            self.logger.log("[green]new settings are configured[/green]")
