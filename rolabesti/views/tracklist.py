import random
from time import sleep

import typer

from .utils import play_audio
from rolabesti.logger import Logger
from rolabesti.models import FIELD_FILTERS, Track
from rolabesti.utils import length_to_string


SUMMARY_FIELDS = ("artist", "album", "genre", "place")


class Tracklist:
    def __init__(self, tracks: list[Track], count: int, length: int) -> None:
        self.tracks = tracks
        self.count = count
        self.length = length
        self.logger = Logger()

    def sort(self, sorting: str) -> None:
        """Sort tracks by path on `sorting` order."""
        match sorting:
            case "asc":
                self.tracks.sort(key=lambda track: track.path)
            case "desc":
                self.tracks.sort(key=lambda track: track.path, reverse=True)
            case "random":
                random.shuffle(self.tracks)

    def truncate(self, max_tracklist_length: int) -> None:
        """
        Truncate tracklist so that the length is less than or equal to max_tracklist_length.
        Preconditions:
            -self.count >= 1
            -any track length <= max_tracklist_length
        """
        length = 0
        for i, track in enumerate(self.tracks):
            if length + track.length <= max_tracklist_length:
                length += track.length
            else:
                i -= 1
                break
        self.tracks = self.tracks[:i + 1]
        self.count = i + 1
        self.length = length

    def print(self) -> None:
        """
        Print tracklist and summary.
        Precondition: self.count >= 1
        """
        self.logger.log("[italic green]--------------- TRACKLIST ---------------[/italic green]")

        summary_fields = {summary_field: set() for summary_field in SUMMARY_FIELDS}
        for track in self.tracks:
            for summary_field in SUMMARY_FIELDS:
                for field in FIELD_FILTERS[summary_field]:
                    if value := getattr(track, field):
                        summary_fields[summary_field].add(value)
                        break
            self.logger.log(str(track))

        self.logger.log("[italic green]--------------- SUMMARY -----------------[/italic green]")
        self.logger.log(f"[bold blue]Tracks[/bold blue]: [bold yellow]{self.count}[/bold yellow]")
        self.logger.log(f"[bold blue]Length[/bold blue]: [bold yellow]{length_to_string(self.length)}[/bold yellow]")

        for summary_field in SUMMARY_FIELDS:
            if summary_fields[summary_field]:
                values = "[bold red] | [/bold red]".join(sorted(summary_fields[summary_field]))
                self.logger.log(f"[bold blue]{summary_field.capitalize()}s[/bold blue]: "
                                f"[bold yellow]{len(summary_fields[summary_field])}[/bold yellow] - "
                                f"[bold green]{values}[/bold green]")

        self.logger.log("[green]-----------------------------------------[/green]")

    def play(self, cli: bool, overlap_length: int) -> None:
        """
        Play and enqueue tracklist in selected app.
        Precondition: self.count >= 1
        """
        if cli:
            for i, track in enumerate(self.tracks):
                self.logger.log(f"[green]playing --> [/green]{track}")
                play_audio(track.path)

                # Adjust waiting_length. Filter out last track and too short tracks.
                if i < self.count - 1 and overlap_length < track.length:
                    waiting_length = track.length - overlap_length
                else:
                    waiting_length = track.length

                # Wait for the current track to finish playing.
                sleep(waiting_length)
        else:
            self.logger.log("[green]launching default app to play and enqueue tracklist[/green]")

            if typer.launch(str(self.tracks[0].path)) == 0:
                # Wait for the default app to open.
                sleep(3)
            else:
                self.logger.log("[green]default app returned an error[/green]")
                raise typer.Abort()

            for track in self.tracks[1:]:
                typer.launch(str(track.path))
