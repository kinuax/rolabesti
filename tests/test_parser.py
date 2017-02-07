# -*- coding: utf-8 -*-

from unittest.mock import patch

from rolabesti.parser import parse


def test_parse_with_supported_trackpaths():
    place = 'some place'
    genre = 'some genre'
    album = 'some album'
    side = 'some side'
    artist = 'some artist'
    filename = 'some filename'

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/Albums/{}/{}.mp3'.format(place, genre, album, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['place'] == place and track['genre'] == genre and track['album'] == album and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/Albums/{}/{}/{}.mp3'.format(place, genre, album, side, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 5
    assert track['place'] == place and track['genre'] == genre and track['side'] == side and track['album'] == album and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/{}/{}/{}.mp3'.format(place, genre, artist, album, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 5
    assert track['place'] == place and track['genre'] == genre and track['artist'] == artist and track['album'] == album and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/{}/{}/{}/{}.mp3'.format(place, genre, artist, album, side, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 6
    assert track['place'] == place and track['genre'] == genre and track['artist'] == artist and track['album'] == album and track['side'] == side and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/{}/{}.mp3'.format(place, genre, artist, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['place'] == place and track['genre'] == genre and track['artist'] == artist and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/Albums/{}/{}.mp3'.format(place, album, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['place'] == place and track['album'] == album and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/Albums/{}/{}/{}.mp3'.format(place, album, side, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['place'] == place and track['album'] == album and track['side'] == side and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/{}/{}/{}.mp3'.format(place, artist, album, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['place'] == place and track['artist'] == artist and track['album'] == album and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/{}/{}/{}/{}.mp3'.format(place, artist, album, side, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 5
    assert track['place'] == place and track['artist'] == artist and track['album'] == album and track['side'] == side and track['filename'] == filename

    trackpath = '/path/to/music/directory/Places/{}/{}/{}.mp3'.format(place, artist, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['place'] == place and track['artist'] == artist and track['filename'] == filename

    trackpath = '/path/to/music/directory/Genres/{}/Albums/{}/{}.mp3'.format(genre, album, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['genre'] == genre and track['album'] == album and track['filename'] == filename

    trackpath = '/path/to/music/directory/Genres/{}/Albums/{}/{}/{}.mp3'.format(genre, album, side, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['genre'] == genre and track['album'] == album and track['side'] == side and track['filename'] == filename

    trackpath = '/path/to/music/directory/Genres/{}/{}/{}/{}.mp3'.format(genre, artist, album, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['genre'] == genre and track['artist'] == artist and track['album'] == album and track['filename'] == filename

    trackpath = '/path/to/music/directory/Genres/{}/{}/{}/{}/{}.mp3'.format(genre, artist, album, side, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 5
    assert track['genre'] == genre and track['artist'] == artist and track['album'] == album and track['side'] == side and track['filename'] == filename

    trackpath = '/path/to/music/directory/Genres/{}/{}/{}.mp3'.format(genre, artist, filename)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['genre'] == genre and track['artist'] == artist and track['filename'] == filename


@patch('rolabesti.parser.getLogger')
def test_parse_with_unsupported_trackpaths(get_logger_mock):
    trackpath = '/path/to/music/directory/Places/{}/{}.mp3'
    track = parse(trackpath)
    assert track == {}
    assert get_logger_mock.return_value.info.called

    get_logger_mock.return_value.reset_mock()
    trackpath = '@#wW#$DS23VTW#@%$wsVWExEW234ER^#^#$%'
    track = parse(trackpath)
    assert track == {}
    assert get_logger_mock.return_value.info.called
