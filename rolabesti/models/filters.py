FIELD_FILTERS = {
    "artist": ("path_artist", "id3_artist"),
    "title": ("id3_title", "path_title"),
    "album": ("path_album", "id3_album"),
    "genre": ("path_genre", "id3_genre"),
    "place": ("path_place",),
}
LENGTH_FILTERS = {"max_track_length", "min_track_length"}
SEARCH_FILTERS = set.union(set(FIELD_FILTERS), LENGTH_FILTERS)
