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
    (Path() / "Places" / place / "Genres" / genre / "Albums" / album / side / f"{title}.mp3", 3),
    (Path() / "Places" / place / "Genres" / genre / "Albums" / album / f"{title}.mp3", 3),
    (Path() / "Places" / place / "Genres" / genre / artist / album / side / f"{title}.mp3", 4),
    (Path() / "Places" / place / "Genres" / genre / artist / album / f"{title}.mp3", 4),
    (Path() / "Places" / place / "Genres" / genre / artist / f"{title}.mp3", 3),
    (Path() / "Places" / place / "Genres" / genre / f"{title}.mp3", 2),
    (Path() / "Places" / place / "Albums" / album / side / f"{title}.mp3", 2),
    (Path() / "Places" / place / "Albums" / album / f"{title}.mp3", 2),
    (Path() / "Places" / place / artist / album / side / f"{title}.mp3", 3),
    (Path() / "Places" / place / artist / album / f"{title}.mp3", 3),
    (Path() / "Places" / place / artist / f"{title}.mp3", 2),
    (Path() / "Places" / place / f"{title}.mp3", 1),
    (Path() / "Genres" / genre / "Albums" / album / side / f"{title}.mp3", 2),
    (Path() / "Genres" / genre / "Albums" / album / f"{title}.mp3", 2),
    (Path() / "Genres" / genre / artist / album / side / f"{title}.mp3", 3),
    (Path() / "Genres" / genre / artist / album / f"{title}.mp3", 3),
    (Path() / "Genres" / genre / artist / f"{title}.mp3", 2),
    (Path() / "Genres" / genre / f"{title}.mp3", 1),
    (Path() / "Albums" / album / side / f"{title}.mp3", 1),
    (Path() / "Albums" / album / f"{title}.mp3", 1),
    (Path() / "Artists" / artist / album / side / f"{title}.mp3", 2),
    (Path() / "Artists" / artist / album / f"{title}.mp3", 2),
    (Path() / "Artists" / artist / f"{title}.mp3", 1),
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
    Path() / "Places" / place,
    Path() / "Albums" / album,
    Path() / "some" / "path",
])
def test_parse_path_fields_with_unsupported_trackpaths(
    trackpath: Path,
) -> None:
    path_fields = parser._parse_path_fields(trackpath)
    assert path_fields == {}
