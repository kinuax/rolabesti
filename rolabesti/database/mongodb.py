import re
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from pymongo import MongoClient, collection

from .db import DB
from rolabesti.models import FIELD_FILTERS


class MongoDB(DB):
    def __init__(self, mongodb_host: str, mongodb_port: int, mongodb_dbname: str, mongodb_colname: str) -> None:
        self.mongodb_host = mongodb_host
        self.mongodb_port = mongodb_port
        self.mongodb_dbname = mongodb_dbname
        self.mongodb_colname = mongodb_colname

    def count(self) -> int:
        with self._get_collection() as collection:
            return collection.count_documents({})

    def empty(self) -> None:
        with self._get_collection() as collection:
            collection.delete_many({})

    def insert_many(self, tracks: list[dict]) -> None:
        with self._get_collection() as collection:
            collection.insert_many(tracks)

    def search(self, search_filters: dict) -> Generator[dict, None, None]:
        mongodb_filters = self._get_mongodb_filters(search_filters)
        with self._get_collection() as collection:
            with collection.find(mongodb_filters) as cursor:
                for track in cursor:
                    yield track

    def update_one(self, path: Path, field: str, value: str | int) -> None:
        with self._get_collection() as collection:
            collection.update_one({"path": str(path)}, {"$set": {field: value}})

    @contextmanager
    def _get_collection(self) -> collection.Collection:
        """Get PyMongo collection."""
        client = MongoClient(host=self.mongodb_host, port=self.mongodb_port)
        yield client[self.mongodb_dbname][self.mongodb_colname]
        client.close()

    @staticmethod
    def _get_mongodb_filters(search_filters: dict) -> dict[str, list[dict]]:
        """Get MongoDB filters from search filters."""
        mongodb_filters = [{}]

        # Get length filters.
        length_filters = {}
        if (max_track_length := search_filters.get("max_track_length")) is not None:
            length_filters["$lte"] = max_track_length
        if (min_track_length := search_filters.get("min_track_length")) is not None:
            length_filters["$gte"] = min_track_length
        if length_filters:
            mongodb_filters.append({"length": length_filters})

        # Get field filters.
        for field_filter in set.intersection(set(FIELD_FILTERS), set(search_filters)):
            filter_value = re.compile(search_filters[field_filter], re.IGNORECASE)
            fields = FIELD_FILTERS[field_filter]
            if len(fields) == 1:
                filter_ = {fields[0]: filter_value}
            else:
                filter_ = {"$or": [{fields[0]: filter_value}, {fields[1]: filter_value}]}
            mongodb_filters.append(filter_)

        return {"$and": mongodb_filters}
