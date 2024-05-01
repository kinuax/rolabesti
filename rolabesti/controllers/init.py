from pathlib import Path

from .controller import Controller
from .parser import Parser


BATCH_SIZE = 100
COUNTS = (100, 500, 1000, 2000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000)


class InitController(Controller):
    def __call__(self) -> None:
        """Traverse directories to parse and insert tracks in database."""
        self.logger.log(f"[green]initializing database with metadata of mp3 tracks located at[/green] "
                        f"[blue]{self.parameters['music_directory']}[/blue]")

        self.db.empty()
        tracks = []
        count = 0
        parser = Parser()
        for trackpath in Path(self.parameters["music_directory"]).glob("**/*.[mM][pP]3"):
            if track := parser.parse(trackpath):
                tracks.append(track.model_dump(exclude_none=True))
                count += 1
                if count % BATCH_SIZE == 0:
                    self.db.insert_many(tracks)
                    tracks.clear()
                    if count in COUNTS:
                        self.logger.log(f"[yellow]{count}[/yellow] [green]tracks loaded so far[/green]")

        if tracks:
            self.db.insert_many(tracks)

        self.logger.log(f"[yellow]{count}[/yellow] [green]track{'s'[:count!=1]} loaded in total[/green]")
