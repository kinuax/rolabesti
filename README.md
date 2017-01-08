rolabesti - Music Library Manager
=================================

- [Motivation](#motivation)
- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Comments](#comments)

Motivation
----------

The main motivation is to answer a question that music fans, DJs, bartenders and melomaniacs with tons of audio files may face: 'What music do I play?' That is, 'what genre do I want now?' or 'which random songs can fill up the time I am able to listen?' are the type of questions that **rolabesti** replies.

Description
----------

**rolabesti** is an application to manage a music library, performing the following actions on mp3 files: parsing, searching, playing, enqueueing, copying, and tagging.

Requirements
------------

- Unix environment.
- Python 3.x. An isolated virtual environment is very recommended. More info about virtualenv [here](https://github.com/pypa/virtualenv).
- MongoDB running instance.
- vlc player. Optional, only required if `PLAYING_MODE` setting is `vlc`.

Installation
------------

1) Clone the repository.

    git clone https://github.com/kinuax/rolabesti.git

2) Install Python packages.

    cd rolabesti
    pip install -r requirements.txt

Configuration
-------------

1) Organize the music library. Choose a music directory `MUSIC_DIR` and locate the audio files applying any of these paths, where `<place>`, `<genre>`, `<artist>`, `<album>`, `<side>` and `<track>` are placeholders and square brackets mean optional.

- `MUSIC_DIR/Places/<place>/Genres/<genre>/Albums/<album>/[<side>/]<track>.mp3`
- `MUSIC_DIR/Places/<place>/Genres/<genre>/<artist>/<album>/[<side>/]<track>.mp3`
- `MUSIC_DIR/Places/<place>/Genres/<genre>/<artist>/<track>.mp3`
- `MUSIC_DIR/Places/<place>/Albums/<album>/[<side>/]<track>.mp3`
- `MUSIC_DIR/Places/<place>/<artist>/<album>/[<side>/]<track>.mp3`
- `MUSIC_DIR/Places/<place>/<artist>/<track>.mp3`
- `MUSIC_DIR/Genres/<genre>/Albums/<album>/[<side>/]<track>.mp3`
- `MUSIC_DIR/Genres/<genre>/<artist>/<album>/[<side>/]<track>.mp3`
- `MUSIC_DIR/Genres/<genre>/<artist>/<track>.mp3`

2) Edit `settings.py`.

- `LOG_DIR`: path to store the logs.
- `MUSIC_DIR`: path to the music directory.
- `MIN_TRACK_LENGTH`: default minimum track length in minutes, corresponding to the MIN argument.
- `MAX_TRACK_LENGTH`: default maximum track length in minutes, corresponding to the MAX argument.
- `MAX_TRACKLIST_LENGTH`: default maximum tracklist length in minutes, corresponding to the MAX_TRACKLIST_LENGTH argument.
- `SORTING`: default tracklist sorting, corresponding to the SORTING argument; choices are asc (ascending), desc (descending) and random.
- `PLAYING_MODE`: playing mode; choices are `shell` (play tracks on the shell) and `vlc` (play tracks on the vlc player, opening it if necessary).
- `OVERLAP_LENGTH`: length in seconds to overlap previous and following tracks, in the range [0, 30].
- `MONGO_HOST`: MongoDB host.
- `MONGO_PORT`: MongoDB port.
- `MONGO_DBNAME`: MongoDB database name.
- `MONGO_COLNAME`: MongoDB collection name.

3) Load the database.

    python3 rolabesti.py load

4) If `PLAYING_MODE` setting is `vlc`, vlc player has to be configured as one running instance.
- Preferences/Interface/Playlist and Instances/Allow only one instance: `enabled`
- Preferences/Interface/Playlist and Instances/Enqueue items into playlist in one instance mode: `enabled`

Usage
-----

    python3 rolabesti.py [-h] SUBCOMMAND [ARGUMENTS]

You can check the arguments for each subcommand with:

    python3 rolabesti.py SUBCOMMAND -h

Let's see some usage examples.

To play two hours of rock music, limiting the track length to 10 minutes, with random sorting:

    python3 rolabesti.py play -g rock -l 120 --max 10 -s random

To play an hour of rap music from Iceland, skipping intro and outro tracks (less than 2 minutes length), with ascending sorting:

    python3 rolabesti.py play -g rap -l 60 -p Iceland --min 2 -s asc


Comments
--------

- Feedback, bugs and suggestions are very welcome. =)
