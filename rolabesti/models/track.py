from pydantic import BaseModel, FilePath, NonNegativeInt, field_serializer

from .filters import FIELD_FILTERS
from rolabesti.utils import length_to_string


class Track(BaseModel):
    path: FilePath
    length: NonNegativeInt
    id3_artist: str | None = None
    id3_title: str | None = None
    id3_album: str | None = None
    id3_genre: str | None = None
    path_artist: str | None = None
    path_title: str | None = None
    path_album: str | None = None
    path_genre: str | None = None
    path_place: str | None = None

    @field_serializer("path")
    def serialize_path(self, path: FilePath, _info):
        return str(path)

    def __str__(self):
        track_fields = []
        for filter_, fields in FIELD_FILTERS.items():
            for field in fields:
                if value := getattr(self, field):
                    track_fields.append(f"[bold blue]{filter_.capitalize()}[/bold blue] = "
                                        f"[bold green]{value}[/bold green]")
                    break
        track_fields.append(f"[bold blue]Length[/bold blue] = [bold green]{length_to_string(self.length)}[/bold green]")
        return "[bold red] | [/bold red]".join(track_fields)
