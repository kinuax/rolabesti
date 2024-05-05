from os.path import exists

import typer

from .controller import Controller
from rolabesti.models import LENGTH_FILTERS, SEARCH_FILTERS, Track
from rolabesti.views import Tracklist


class SearchController(Controller):
    def __call__(self) -> None:
        """
        Set tracklist based on parameters.
        Postcondition: tracklist.count >= 1
        """
        # Ensure database is initialized.
        if self.db.count() == 0:
            self.logger.log("[green]the database has no tracks - run `rolabesti init` to initialize it[/green]")
            raise typer.Exit()
        self.tracklist = self._get_tracklist()
        # Ensure there is at least one matching track.
        if self.tracklist.count == 0:
            self.logger.log("[green]no tracks match your search criteria[/green]")
            raise typer.Exit()

    def _get_tracklist(self) -> Tracklist:
        """Search, build, and return tracklist."""
        tracks = []
        count = 0
        length = 0
        for track in self.db.search(self._get_search_filters()):
            # Ensure track exists in file system.
            if exists(track["path"]):
                tracks.append(Track(**track))
                count += 1
                length += track["length"]
        return Tracklist(tracks, count, length)

    def _get_search_filters(self) -> dict:
        """Get search filters from parameters."""
        search_filters = {}
        for search_filter in set.intersection(SEARCH_FILTERS, set(self.parameters)):
            if (value := self.parameters[search_filter]) is not None:
                # Disable zero length filters.
                if not (search_filter in LENGTH_FILTERS and value == 0):
                    search_filters[search_filter] = value
        return search_filters
