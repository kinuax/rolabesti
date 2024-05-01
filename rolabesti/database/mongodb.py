import re
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from pymongo import MongoClient, collection

from .db import DB
from rolabesti.conf.settings import MONGO_HOST, MONGO_PORT, MONGO_DBNAME, MONGO_COLNAME
from rolabesti.models import FIELD_FILTERS


class MongoDB(DB):
    def __init__(
        self,
        mongo_host: str = MONGO_HOST,
        mongo_port: int = MONGO_PORT,
        mongo_dbname: str = MONGO_DBNAME,
        mongo_colname: str = MONGO_COLNAME,
    ) -> None:
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_dbname = mongo_dbname
        self.mongo_colname = mongo_colname

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
        client = MongoClient(host=self.mongo_host, port=self.mongo_port)
        yield client[self.mongo_dbname][self.mongo_colname]
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
