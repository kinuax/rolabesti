rolabesti - Music library manager
=================================

- [Motivation](#motivation)
- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Options](#options)
- [Comments](#comments)

Motivation
----------

The main motivation is to answer a question that music fans, DJs, bartenders and melomaniacs with tons of audio files may face: 'What music do I play?' That is, 'what genre do I want now?' or 'which random songs can fill up the time I am able to listen?' are the type of questions that **rolabesti** replies.

Description
----------

**rolabesti** is a command-line program to manage a music library, achieving the following operations on mp3 files: parsing, searching, playing, enqueueing, copying, listing and tagging.

Requirements
------------

- Unix environment.
- Python 2.7.
- MongoDB.
- vlc player.

Installation
------------

1) Clone the repository.

    git clone https://github.com/kinuax/rolabesti.git

2) Install Python packages.

    pip install -r requirements.txt

Configuration
-------------

1) Organize the music library. Choose a music directory (MUSIC_DIR) and locate the audio files applying any of these paths, where \<place\>, \<genre\>, \<artist\>, \<album\>, \<side\> and \<track\> are placeholders and square brackets denote optional element:

- MUSIC_DIR/Places/\<place\>/Genres/\<genre\>/Albums/\<album\>/[\<side\>/]\<track\>.mp3
- MUSIC_DIR/Places/\<place\>/Genres/\<genre\>/\<artist>/\<album\>/[\<side\>/]\<track\>.mp3
- MUSIC_DIR/Places/\<place\>/Genres/\<genre\>/\<artist>/\<track\>.mp3
- MUSIC_DIR/Places/\<place\>/Albums/\<album\>/[\<side\>/]\<track\>.mp3
- MUSIC_DIR/Places/\<place\>/\<artist>/\<album\>/[\<side\>/]\<track\>.mp3
- MUSIC_DIR/Places/\<place\>/\<artist>/\<track\>.mp3
- MUSIC_DIR/Genres/\<genre\>/Albums/\<album\>/[\<side\>/]\<track\>.mp3
- MUSIC_DIR/Genres/\<genre\>/\<artist>/\<album\>/[\<side\>/]\<track\>.mp3
- MUSIC_DIR/Genres/\<genre\>/\<artist>/\<track\>.mp3

2) Customize `settings.py`. At least `MUSIC_DIR` should me updated with the chosen directory:

- `DB_DIR`: path to store the database.
- `LOG_DIR`: path to store the logs.
- `MUSIC_DIR`: path to the music directory.
- `METHOD`: default method to run, corresponding to the METHOD option; choices are build (build the database), play (play and enqueue tracks with vlc), copy (copy tracks to the destiny folder), list (show tracks information and summary) and tag (write ID3 tags).
- `SORTING`: default tracklist sorting, corresponding to the SORTING option; choices are asc (ascending), desc (descending) and random.
- `TOTAL_LENGTH`: default maximum tracklist length in minutes, corresponding to the TOTAL_LENGTH option.
- `MIN_TRACK_LENGTH`: default minimum track length in minutes, corresponding to the MIN option.
- `MAX_TRACK_LENGTH`: default maximum track length in minutes, corresponding to the MAX option.
- `MONGO_HOST`: MongoDB host.
- `MONGO_PORT`: MongoDB port.
- `MONGO_DBNAME`: MongoDB database name.
- `MONGO_COLNAME`: MongoDB collection name.

3) Build the database.

    cd rolabesti
    python rolabesti.py -m build

Usage
-----

    python rolabesti.py [OPTIONS]

Some usage examples.

To play two hours of rock music, limiting the track length to 10 minutes, with random sorting:

    python rolabesti.py -m play -t 120 -g rock --max 10 -s random

To play an hour of rap music from Iceland, skipping intro and outro tracks (less than 2 minutes length), with ascending sorting:

    python rolabesti.py -m play -t 60 -g rap -p iceland --min 2 -s asc

Options
-------

    -h, --help                                      show this help message and exit
    -m METHOD, --method METHOD                      method to run
    -s SORTING, --sorting SORTING                   tracklist sorting
    -t TOTAL_LENGTH, --total_length TOTAL_LENGTH    maximum tracklist length, in minutes
    --min MIN                                       minimum track length to search, in minutes
    --max MAX                                       maximum track length to search, in minutes
    -p PLACE, --place PLACE                         track place to search
    -g GENRE, --genre GENRE                         track genre to search
    -ar ARTIST, --artist ARTIST                     track artist to search
    -al ALBUM, --album ALBUM                        track album to search
    -d DESTINY, --destiny DESTINY                   directory to copy tracks, required if method is copy

Comments
--------

- Feedback, bugs and suggestions are very welcome.
