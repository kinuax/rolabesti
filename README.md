# rolabesti - CLI app to manage, search, and play collections of mp3 tracks.

[![Stable Version](https://img.shields.io/pypi/v/rolabesti?labelColor=202235&color=edb641&logo=python&logoColor=edb641)](https://pypi.org/project/rolabesti/)
[![Python Versions](https://img.shields.io/pypi/pyversions/rolabesti?labelColor=202235&color=edb641&logo=python&logoColor=edb641)](https://pypi.org/project/rolabesti/)
[![License - MIT](https://img.shields.io/badge/license-MIT-202235.svg?logo=python&labelColor=202235&color=edb641&logoColor=edb641)](https://spdx.org/licenses/)
[![Downloads](https://static.pepy.tech/badge/rolabesti)](https://pepy.tech/project/rolabesti)

[![Typer](https://img.shields.io/badge/Typer-0.12.3-009485?style=for-the-badge&logo=fastapi&logoColor=white)](https://typer.tiangolo.com/)
[![Rich](https://img.shields.io/badge/rich-13.7.1-0094?style=for-the-badge&logo=rich&logoColor=white)](https://rich.readthedocs.io/en/latest/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.7.0-e92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/latest/)
[![Mutagen](https://img.shields.io/badge/mutagen-1.47.0-009758?style=for-the-badge&logo=mutagen&logoColor=red)](https://rich.readthedocs.io/en/latest/)

-   [Motivation](#motivation)
-   [Description](#description)
-   [Key Features](#key-features)
-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Preparation](#preparation)
-   [Examples](#examples)
-   [Usage](#usage)

## Motivation

The main purpose of this app is to give a solution to the scenario that
some music fan, DJ, bartender, podcast enthusiast, or melomaniac may face:
"Having a great bunch of songs, what music do I play now?". For instance,
"what random songs of this artist or that genre can fill the next hour?"
is the question that **rolabesti** answers.

## Description

**rolabesti** is a CLI application to manage collections of mp3 tracks,
supporting these actions: loading metadata to database, parsing,
searching, listing, playing, enqueueing, copying, and tagging.

## Key Features

- Any audio file in mp3 format serves as raw material for the app. 
- Select random and sorted songs matching multiple criteria.
- Play music directly in the terminal or send the tracklist to the default app.
- Tracks missing ID3 tags can be classified and leveraged.
- Mixer to avoid silence between songs.
- Selected tracklist length becomes a useful timer. 
- OS independent.

## Requirements

-   Python 3.10+.

## Installation

- The recommended way to install is using [pipx](https://pipx.pypa.io/stable/installation/#installing-pipx). 

```bash
pipx install rolabesti
```

## Preparation

All mp3 files located at user's `Music` directory compose the music collection.
Optionally, folders can be labeled to apply any of the following patterns.
This way the database is better populated with the path fields and the accuracy
of the matching tracks improves.

- `Artists/<artist>/<title>.mp3`
- `Artists/<artist>/<album>/[<side>/]<title>.mp3`
- `Albums/<album>/[<side>/]<title>.mp3`
- `Genres/<genre>/<title>.mp3`
- `Genres/<genre>/<artist>/<title>.mp3`
- `Genres/<genre>/<artist>/<album>/[<side>/]<title>.mp3`
- `Genres/<genre>/Albums/<album>/[<side>/]<title>.mp3`
- `Places/<place>/<title>.mp3`
- `Places/<place>/<artist>/<title>.mp3`
- `Places/<place>/<artist>/<album>/[<side>/]<title>.mp3`
- `Places/<place>/Albums/<album>/[<side>/]<title>.mp3`
- `Places/<place>/Genres/<genre>/<title>.mp3`
- `Places/<place>/Genres/<genre>/<artist>/<title>.mp3`
- `Places/<place>/Genres/<genre>/<artist>/<album>/[<side>/]<title>.mp3`
- `Places/<place>/Genres/<genre>/Albums/<album>/[<side>/]<title>.mp3`

`<title>`, `<artist>`, `<album>`, `<side>` (optional), `<genre>`, and `<place>` are placeholders.

The minimum steps to start playing are:

```bash
rolabesti init
rolabesti play
```

Optionally, when the default app is selected as the player, `vlc` is recommended with this configuration:

- Tools/Preferences/Interface/Playlist and Instances
  - Allow only one instance: `checked`
  - Enqueue items into playlist in one instance mode: `checked`

## Examples

To play two hours of rock music, limiting the track length to 5
minutes, with random sorting:

```bash
rolabesti play -l 120 -g rock --max 5 -s random
```

To play an hour of rap music from Iceland, skipping intro and outro
tracks (less than 2 minutes length), with ascending sorting:

```bash
rolabesti play -l 60 -g rap -p Iceland --min 2 -s asc
```

## Usage

**Usage**:

```bash
rolabesti [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Show the application version and exit.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `-h, --help`: Show this message and exit.

**Commands**:

* `config`: Manage configuration settings.
* `init`: Initialize database.
* `list`: List matching tracks.
* `play`: Play and enqueue matching tracks.
* `copy`: Copy matching tracks to a directory.
* `tag`: Update ID3 tags with path fields (file and database).

## `rolabesti config`

Manage configuration settings.

**Usage**:

```bash
rolabesti config [OPTIONS]
```

**Options**:

* `--list`: List configuration settings.
* `--reset`: Reset configuration settings.
* `-h, --help`: Show this message and exit.

**Main settings**:

* `--max INTEGER RANGE [x>=0]`: Set default maximum track length in minutes (0 means disabled).
* `--min INTEGER RANGE [x>=0]`: Set default minimum track length in minutes.
* `-l, --length INTEGER RANGE [x>=0]`: Set default maximum tracklist length in minutes (0 means disabled).
* `-s, --sorting [asc|desc|random]`: Set default order by track path.

**Play settings**:

* `-o, --overlap-length INTEGER RANGE [0<=x<=30]`: Set default overlap length in seconds between two consecutive tracks (0 means disabled).

**Database settings**:

* `--music-directory DIRECTORY`: Set default path to mp3 files.

**Copy settings**:

* `--copy-directory DIRECTORY`: Set default path to destiny directory.

## `rolabesti init`

Initialize database.

**Usage**:

```bash
rolabesti init [OPTIONS]
```

**Options**:

* `-d, --music-directory DIRECTORY`: Path to mp3 files. [default: /home/user/Music]
* `-h, --help`: Show this message and exit.

## `rolabesti list`

List matching tracks.

**Usage**:

```bash
rolabesti list [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.

**Search filters**:

* `-ar, --artist TEXT`: Track artist.
* `-t, --title TEXT`: Track title.
* `-al, --album TEXT`: Track album.
* `-g, --genre TEXT`: Track genre.
* `-p, --place TEXT`: Track place.
* `--max INTEGER RANGE [x>=0]`: Maximum track length in minutes (0 means disabled). [default: 10]
* `--min INTEGER RANGE [x>=0]`: Minimum track length in minutes. [default: 0]

**Tracklist selectors**:

* `-s, --sorting [asc|desc|random]`: Order by track path. [default: random]

## `rolabesti play`

Play and enqueue matching tracks.

**Usage**:

```bash
rolabesti play [OPTIONS]
```

**Options**:

* `--cli / --no-cli`: Select cli or default app.  [default: cli]
* `-o, --overlap-length INTEGER RANGE [0<=x<=30]`: Overlap length in seconds between two consecutive tracks (only with --cli, 0 means disabled). [default: 3]
* `-h, --help`: Show this message and exit.

**Search filters**:
 
* `-ar, --artist TEXT`: Track artist.
* `-t, --title TEXT`: Track title.
* `-al, --album TEXT`: Track album.
* `-g, --genre TEXT`: Track genre.
* `-p, --place TEXT`: Track place.
* `--max INTEGER RANGE [x>=0]`: Maximum track length in minutes (0 means disabled). [default: 10]
* `--min INTEGER RANGE [x>=0]`: Minimum track length in minutes. [default: 0]

**Tracklist selectors**:

* `-l, --length INTEGER RANGE [x>=0]`: Maximum tracklist length in minutes (0 means disabled). [default: 60]
* `-s, --sorting [asc|desc|random]`: Order by track path. [default: random]

## `rolabesti copy`

Copy matching tracks to a directory.

**Usage**:

```bash
rolabesti copy [OPTIONS]
```

**Options**:

* `-d, --copy-directory DIRECTORY`: Path to destiny directory. [default: /home/user/Documents]
* `-h, --help`: Show this message and exit.

**Search filters**:

* `-ar, --artist TEXT`: Track artist.
* `-t, --title TEXT`: Track title.
* `-al, --album TEXT`: Track album.
* `-g, --genre TEXT`: Track genre.
* `-p, --place TEXT`: Track place.
* `--max INTEGER RANGE [x>=0]`: Maximum track length in minutes (0 means disabled). [default: 10]
* `--min INTEGER RANGE [x>=0]`: Minimum track length in minutes. [default: 0]

**Tracklist selectors**:

* `-l, --length INTEGER RANGE [x>=0]`: Maximum tracklist length in minutes (0 means disabled). [default: 60]
* `-s, --sorting [asc|desc|random]`: Order by track path. [default: random]

## `rolabesti tag`

Update ID3 tags with path fields (file and database).

**Usage**:

```bash
rolabesti tag [OPTIONS]
```

**Options**:

* `--id3-tag [artist|title|album|genre]`: ID3 tag to be updated. [required]
* `-h, --help`: Show this message and exit.

**Search filters**:

* `-ar, --artist TEXT`: Track artist.
* `-t, --title TEXT`: Track title.
* `-al, --album TEXT`: Track album.
* `-g, --genre TEXT`: Track genre.
* `-p, --place TEXT`: Track place.
* `--max INTEGER RANGE [x>=0]`: Maximum track length in minutes (0 means disabled). [default: 10]
* `--min INTEGER RANGE [x>=0]`: Minimum track length in minutes. [default: 0]
