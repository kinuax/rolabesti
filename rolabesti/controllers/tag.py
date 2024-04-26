import os
from os.path import exists

from .search import SearchController
from .utils import get_id3_dict


class TagController(SearchController):
    def __call__(self) -> None:
        super().__call__()
        id3_tag = self.parameters["id3_tag"]
        id3_field = f"id3_{id3_tag}"
        path_field = f"path_{id3_tag}"
        count = 0
        msg = "[green]unable to tag track [/green]"
        for track in self.tracklist.tracks:
            path_value = getattr(track, path_field)
            if path_value is None or path_value == "":
                self.logger.log(msg + f"[blue]{track.path}[/blue][green] - no {id3_tag} in path[/green]")
                continue
            if not exists(track.path):
                self.logger.log(msg + f"[blue]{track.path}[/blue][green] - file does not exist[/green]")
                continue
            if not os.access(track.path, os.W_OK):
                self.logger.log(msg + f"[blue]{track.path}[/blue][green] - missing write permissions[/green]")
                continue
            if (id3_dict := get_id3_dict(track.path)) is None:
                self.logger.log(msg + f"[blue]{track.path}[/blue][green] - missing ID3 tags[/green]")
                continue

            # Update ID3 tag with path field in file.
            id3_dict[id3_tag] = path_value
            id3_dict.save()

            # Update ID3 tag with path field in database.
            self.db.update_one(track.path, id3_field, path_value)

            count += 1
            self.logger.log(f"[green]track[/green] [blue]{track.path}[/blue] [green]is tagged with {id3_tag}[/green]")

        self.logger.log(f"[yellow]{count}[/yellow] [green]track{'s'[:count != 1]} tagged[/green]")
