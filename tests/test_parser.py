# -*- coding: utf-8 -*-

from unittest.mock import patch

from rolabesti.parser import parse


def test_parse_with_supported_trackpaths():
    place = 'some place'
    genre = 'some genre'
    album = 'some album'
    side = 'some side'
    artist = 'some artist'
    title = 'some title'

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/Albums/{}/{}.mp3'.format(place, genre, album, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['place'] == place and track['genre'] == genre and track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/Albums/{}/{}/{}.mp3'.format(place, genre, album, side, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 5
    assert track['place'] == place and track['genre'] == genre and track['side'] == side and track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/{}/{}/{}.mp3'.format(place, genre, artist, album, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 5
    assert track['place'] == place and track['genre'] == genre and track['artist'] == artist and track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/{}/{}/{}/{}.mp3'.format(place, genre, artist, album, side, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 6
    assert track['place'] == place and track['genre'] == genre and track['artist'] == artist and track['album'] == album and track['side'] == side and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/{}/{}.mp3'.format(place, genre, artist, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['place'] == place and track['genre'] == genre and track['artist'] == artist and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/Genres/{}/{}.mp3'.format(place, genre, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['place'] == place and track['genre'] == genre and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/{}.mp3'.format(place, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 2
    assert track['place'] == place and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/Albums/{}/{}.mp3'.format(place, album, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['place'] == place and track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/Albums/{}/{}/{}.mp3'.format(place, album, side, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['place'] == place and track['album'] == album and track['side'] == side and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/{}/{}/{}.mp3'.format(place, artist, album, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['place'] == place and track['artist'] == artist and track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/{}/{}/{}/{}.mp3'.format(place, artist, album, side, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 5
    assert track['place'] == place and track['artist'] == artist and track['album'] == album and track['side'] == side and track['title'] == title

    trackpath = '/path/to/music/directory/Places/{}/{}/{}.mp3'.format(place, artist, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['place'] == place and track['artist'] == artist and track['title'] == title

    trackpath = '/path/to/music/directory/Genres/{}/Albums/{}/{}.mp3'.format(genre, album, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['genre'] == genre and track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/Genres/{}/Albums/{}/{}/{}.mp3'.format(genre, album, side, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['genre'] == genre and track['album'] == album and track['side'] == side and track['title'] == title

    trackpath = '/path/to/music/directory/Genres/{}/{}/{}/{}.mp3'.format(genre, artist, album, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['genre'] == genre and track['artist'] == artist and track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/Genres/{}/{}/{}/{}/{}.mp3'.format(genre, artist, album, side, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 5
    assert track['genre'] == genre and track['artist'] == artist and track['album'] == album and track['side'] == side and track['title'] == title

    trackpath = '/path/to/music/directory/Genres/{}/{}/{}.mp3'.format(genre, artist, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['genre'] == genre and track['artist'] == artist and track['title'] == title

    trackpath = '/path/to/music/directory/Genres/{}/{}.mp3'.format(genre, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 2
    assert track['genre'] == genre and track['title'] == title

    trackpath = '/path/to/music/directory/Artists/{}/{}/{}/{}.mp3'.format(artist, album, side, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 4
    assert track['artist'] == artist and track['album'] == album and track['side'] == side and track['title'] == title

    trackpath = '/path/to/music/directory/Artists/{}/{}/{}.mp3'.format(artist, album, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['artist'] == artist and track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/Artists/{}/{}.mp3'.format(artist, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 2
    assert track['artist'] == artist and track['title'] == title

    trackpath = '/path/to/music/directory/Albums/{}/{}/{}.mp3'.format(album, side, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 3
    assert track['album'] == album and track['side'] == side and track['title'] == title

    trackpath = '/path/to/music/directory/Albums/{}/{}.mp3'.format(album, title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 2
    assert track['album'] == album and track['title'] == title

    trackpath = '/path/to/music/directory/{}.mp3'.format(title)
    track = parse(trackpath)
    assert type(track) == dict and len(track) == 1
    assert track['title'] == title


@patch('rolabesti.parser.getLogger')
def test_parse_with_unsupported_trackpaths(get_logger_mock):
    trackpath = '/path/to/music/directory/Places/place/title.ogg'
    track = parse(trackpath)
    assert track == {}
    assert get_logger_mock.return_value.info.called

    get_logger_mock.return_value.reset_mock()
    trackpath = '@#wW#$DS23VTW#@%$wsVWExEW234ER^#^#$%'
    track = parse(trackpath)
    assert track == {}
    assert get_logger_mock.return_value.info.called
