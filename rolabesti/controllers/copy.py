from .search import SearchController


class CopyController(SearchController):
    def __call__(self) -> None:
        super().__call__()
        self.tracklist.sort(self.parameters["sorting"])
        if max_tracklist_length := self.parameters["max_tracklist_length"]:
            self.tracklist.truncate(max_tracklist_length)
        self.tracklist.print()
        self.tracklist.copy(self.parameters["copy_directory"])
