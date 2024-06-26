from .search import SearchController


class PlayController(SearchController):
    def __call__(self) -> None:
        super().__call__()
        self.tracklist.sort(self.parameters["sorting"])
        if max_tracklist_length := self.parameters["max_tracklist_length"]:
            self.tracklist.truncate(max_tracklist_length)
        self.tracklist.print()
        self.tracklist.play(self.parameters["cli"], self.parameters["overlap_length"])
