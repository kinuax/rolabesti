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

The main purpose of this tool is to answer a question that music fans, DJs, bartenders or people with tons of music might ask themselves: 'What do I play?' In particular, 'what genre do I want now?' or 'how long am I able to listen?' are the type of questions that **rolabesti** is replying.

Description
----------

**rolabesti** is a command-line program to manage a music library, achieving actions like indexing, searching, playing, copying and listing.

    ./rolabesti.py [OPTIONS]

Requirements
------------

- Unix environment.
- Python 2.7.
- mutagen library.
- vlc player.

Installation
------------

1) Clone the repository.

    git clone https://github.com/kinuax/rolabesti.git

2) Install requirements.

	pip install -r requirements.txt

Configuration
-------------

1) Organize the music library. Choose a music directory (MUSIC_DIR) and locate the audio files, following any of these structures:

- MUSIC_DIR/Places/\<place\>/Genres/\<genre\>/Albums/\<album\>/track.mp3
- MUSIC_DIR/Places/\<place\>/Genres/\<genre\>/\<artist>/\<album\>/track.mp3
- MUSIC_DIR/Places/\<place\>/Genres/\<genre\>/\<artist>/track.mp3
- MUSIC_DIR/Places/\<place\>/Albums/\<album\>/track.mp3
- MUSIC_DIR/Places/\<place\>/\<artist>/\<album\>/track.mp3
- MUSIC_DIR/Places/\<place\>/\<artist>/track.mp3
- MUSIC_DIR/Genres/\<genre\>/Albums/\<album\>/track.mp3
- MUSIC_DIR/Genres/\<genre\>/\<artist>/\<album\>/track.mp3
- MUSIC_DIR/Genres/\<genre\>/\<artist>/track.mp3

Where \<place\>, \<genre\>, \<album\> and \<artist\> are placeholders.

2) Edit MUSIC_DIR variable in settings.py:

- `DB_DIR`: path to store the database.
- `LOG_DIR`: path to store the logs.
- `MUSIC_DIR`: path to the music directory.
- `METHOD`: default method to run, corresponding to the METHOD option; choices are build (build the database index), play (open vlc to play and enqueue found tracks), copy (copy found tracks to destiny folder) and list (show found tracks and summary).
- `SORTING`: default tracklist sorting, corresponding to the SORTING option; choices are asc (ascending), desc (descending) and random.
- `TOTAL_LENGTH`: default maximum tracklist length in minutes, corresponding to the TOTAL_LENGTH option.
- `MIN_TRACK_LENGTH`: default minimum track length in minutes, corresponding to the MIN option.
- `MAX_TRACK_LENGTH`: default maximum track length in minutes, corresponding to the MAX option.

3) Build the database.

	cd rolabesti
	./rolabesti.py -m build

Usage
-----

Some examples of usage.

To play two hours of rock music, limiting the track lenght to 10 minutes, with random sorting:

	./rolabesti.py -m play -t 120 -g rock --max 10 -s random

To play an hour of rap music from Iceland, skipping intro and outro tracks (less than 2 minutes length), with ascending sorting:

	./rolabesti.py -m play -t 60 -g rap -p iceland --min 2 -s asc

Options
-------

  	-h, --help            							show this help message and exit
  	-m METHOD, --method METHOD						method to run
  	-s SORTING, --sorting SORTING 					tracklist sorting
  	-t TOTAL_LENGTH, --total_length TOTAL_LENGTH 	maximum tracklist length in minutes
  	--min MIN             							minimum track length to search, in minutes
  	--max MAX             							maximum track length to search, in minutes
  	-p PLACE, --place PLACE							track place to search
  	-g GENRE, --genre GENRE							track genre to search
  	-ar ARTIST, --artist ARTIST 					track artist to search
  	-al ALBUM, --album ALBUM 						track album to search
  	-d DESTINY, --destiny DESTINY 					directory to copy tracks, required if method is copy

Comments
--------

- Feedback, bugs and suggestions and very welcome.