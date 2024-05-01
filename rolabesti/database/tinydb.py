import re
from collections.abc import Generator
from pathlib import Path

from tinydb import Query, TinyDB as BaseTinyDB, where

from .db import DB
from rolabesti.conf.settings import TINY_FILE
from rolabesti.models import FIELD_FILTERS


class TinyDB(DB):
    def __init__(self) -> None:
        self.db = BaseTinyDB(TINY_FILE)

    def count(self) -> int:
        return len(self.db.all())

    def empty(self) -> None:
        self.db.truncate()

    def insert_many(self, tracks: list[dict]) -> None:
        self.db.insert_multiple(tracks)

    def search(self, search_filters: dict) -> Generator[dict, None, None]:
        tinydb_query = self._get_tinydb_query(search_filters)
        for track in self.db.search(tinydb_query):
            yield track

    def update_one(self, path: Path, field: str, value: str | int) -> None:
        self.db.update({field: value}, Query()["path"] == str(path))

    @staticmethod
    def _get_tinydb_query(search_filters: dict) -> Query:
        """Get TinyDB query from search filters."""
        query = Query().noop()

        # Get length queries.
        if (max_track_length := search_filters.get("max_track_length")) is not None:
            query = query & (where('length') <= max_track_length)
        if (min_track_length := search_filters.get("min_track_length")) is not None:
            query = query & (where('length') >= min_track_length)

        # Get field queries.
        for field_filter in set.intersection(set(FIELD_FILTERS), set(search_filters)):
            filter_value = search_filters[field_filter]
            fields = FIELD_FILTERS[field_filter]
            if len(fields) == 1:
                query = query & where(fields[0]).search(filter_value, flags=re.IGNORECASE)
            else:
                query = query & (where(fields[0]).search(filter_value, flags=re.IGNORECASE) |
                                 where(fields[1]).search(filter_value, flags=re.IGNORECASE))

        return query
