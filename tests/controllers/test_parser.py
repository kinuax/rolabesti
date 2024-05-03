from pathlib import Path

import pytest

from rolabesti.controllers.parser import Parser
from tests.utils import get_random_string


all_path_fields = {
    "place": (place := get_random_string()),
    "genre": (genre := get_random_string()),
    "album": (album := get_random_string()),
    "side": (side := get_random_string()),
    "artist": (artist := get_random_string()),
    "title": (title := get_random_string()),
}
parser = Parser()


@pytest.mark.parametrize("trackpath, length", [
    (Path(f"/path/to/music/directory/Places/{place}/Genres/{genre}/Albums/{album}/{side}/{title}.mp3"), 5),
    (Path(f"/path/to/music/directory/Places/{place}/Genres/{genre}/Albums/{album}/{title}.mp3"), 4),
    (Path(f"/path/to/music/directory/Places/{place}/Genres/{genre}/{artist}/{album}/{side}/{title}.mp3"), 6),
    (Path(f"/path/to/music/directory/Places/{place}/Genres/{genre}/{artist}/{album}/{title}.mp3"), 5),
    (Path(f"/path/to/music/directory/Places/{place}/Genres/{genre}/{artist}/{title}.mp3"), 4),
    (Path(f"/path/to/music/directory/Places/{place}/Genres/{genre}/{title}.mp3"), 3),
    (Path(f"/path/to/music/directory/Places/{place}/Albums/{album}/{side}/{title}.mp3"), 4),
    (Path(f"/path/to/music/directory/Places/{place}/Albums/{album}/{title}.mp3"), 3),
    (Path(f"/path/to/music/directory/Places/{place}/{artist}/{album}/{side}/{title}.mp3"), 5),
    (Path(f"/path/to/music/directory/Places/{place}/{artist}/{album}/{title}.mp3"), 4),
    (Path(f"/path/to/music/directory/Places/{place}/{artist}/{title}.mp3"), 3),
    (Path(f"/path/to/music/directory/Places/{place}/{title}.mp3"), 2),
    (Path(f"/path/to/music/directory/Genres/{genre}/Albums/{album}/{side}/{title}.mp3"), 4),
    (Path(f"/path/to/music/directory/Genres/{genre}/Albums/{album}/{title}.mp3"), 3),
    (Path(f"/path/to/music/directory/Genres/{genre}/{artist}/{album}/{side}/{title}.mp3"), 5),
    (Path(f"/path/to/music/directory/Genres/{genre}/{artist}/{album}/{title}.mp3"), 4),
    (Path(f"/path/to/music/directory/Genres/{genre}/{artist}/{title}.mp3"), 3),
    (Path(f"/path/to/music/directory/Genres/{genre}/{title}.mp3"), 2),
    (Path(f"/path/to/music/directory/Albums/{album}/{side}/{title}.mp3"), 3),
    (Path(f"/path/to/music/directory/Albums/{album}/{title}.mp3"), 2),
    (Path(f"/path/to/music/directory/Artists/{artist}/{album}/{side}/{title}.mp3"), 4),
    (Path(f"/path/to/music/directory/Artists/{artist}/{album}/{title}.mp3"), 3),
    (Path(f"/path/to/music/directory/Artists/{artist}/{title}.mp3"), 2),
    (Path(f"/path/to/music/directory/{title}.mp3"), 1),
])
def test_parse_path_fields_with_supported_trackpaths(
    trackpath: Path,
    length: int,
) -> None:
    path_fields = parser._parse_path_fields(trackpath)
    assert len(path_fields) == length
    for field, value in path_fields.items():
        assert value == all_path_fields[field]


@pytest.mark.parametrize("trackpath", [
    (Path(f"/path/to/music/directory/Places/{place}/Genre/{genre}"), ),
    (Path(f"/path/to/music/directory/Places/{place}/Genre/{genre}/{title}"), ),
    (Path(f"/path/to/music/directory/Places/{place}/{title}.pdf"), ),
    (Path("@#wW#$DS23VTW#@%$wsVWExEW234ER^#^#$%"), ),
])
def test_parse_path_fields_with_unsupported_trackpaths(
    trackpath: Path,
) -> None:
    path_fields = parser._parse_path_fields(trackpath)
    assert path_fields is None
