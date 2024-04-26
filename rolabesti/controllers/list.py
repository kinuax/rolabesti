from .search import SearchController


class ListController(SearchController):
    def __call__(self) -> None:
        super().__call__()
        self.tracklist.sort(self.parameters["sorting"])
        self.tracklist.print()
