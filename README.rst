rolabesti
=========

.. image:: https://img.shields.io/pypi/v/rolabesti.svg
    :target: https://pypi.org/project/rolabesti/

.. image:: https://img.shields.io/pypi/pyversions/rolabesti.svg
    :target: https://pypi.org/project/rolabesti/

.. image:: https://img.shields.io/pypi/wheel/rolabesti.svg
    :target: https://pypi.org/project/rolabesti/

.. image:: https://circleci.com/gh/kinuax/rolabesti.svg?style=shield
    :target: https://circleci.com/gh/kinuax/rolabesti

.. image:: https://img.shields.io/pypi/l/rolabesti.svg
    :target: https://pypi.org/project/rolabesti/

- `Motivation <#motivation>`__
- `Description <#description>`__
- `Requirements <#requirements>`__
- `Installation <#installation>`__
- `Configuration <#configuration>`__
- `Usage <#usage>`__

Motivation
----------

The main motivation is to solve the scenario where some music fan, DJ, bartender, or melomaniac, with tons of mp3 files, may face: 'Considering these tons of mp3 files around, what music do I play?'. For instance, 'what genre would I want to listen?' and 'which random songs can fill up the available time that I have?' are the type of questions that **rolabesti** answers.

Description
-----------

**rolabesti** is a command-line application to manage a music library, performing the following actions on mp3 files: loading to database, parsing, searching, playing, enqueueing, copying, and tagging.

Requirements
------------

-  Linux environment.
-  Python 3.7. A `virtual environment <https://github.com/pypa/virtualenv>`__ is recommended.
-  MongoDB instance.
-  vlc player. When selecting ``shell`` player, only the ``libvlc`` library is required.

Installation
------------

.. code-block:: bash

    $ pip install rolabesti

Configuration
-------------

The default settings can be overriden in ``~/.config/rolabesti/rolabesti.conf``. This configuration file has INI syntax with a unique section named ``[rolabesti]``.

- ``MUSIC_DIR``: path where the mp3 files are located, default is ``~/Music``.
- ``MAX_TRACK_LENGTH``: maximum track length in minutes, corresponding to the ``MAX`` argument, default is ``10``.
- ``MIN_TRACK_LENGTH``: minimum track length in minutes, corresponding to the ``MIN`` argument, default is ``0``.
- ``MAX_TRACKLIST_LENGTH``: maximum tracklist length in minutes, corresponding to the ``MAX_TRACKLIST_LENGTH`` argument; ``0`` denotes no tracklist length limit, default is ``60``.
- ``SORTING``: tracklist sorting, corresponding to the ``SORTING`` argument; choices are ``asc`` (ascending), ``desc`` (descending) and ``random``, default is ``random``.
- ``PLAYER``: player to play and enqueue tracks, corresponding to the ``PLAYER`` argument; choices are ``shell`` (play tracks directly in the shell) and ``vlc`` (play tracks in the vlc player, opening it if necessary), default is ``vlc``.
- ``OVERLAP_LENGTH``: when selecting ``shell`` player, overlap length in seconds between two consecutive tracks, corresponding to the ``OVERLAP_LENGTH`` argument; minimum is ``0``, maximum is ``30``, default is ``3``.
- ``MONGO_HOST``: MongoDB host, default is ``localhost``.
- ``MONGO_PORT``: MongoDB port, default is ``27017``.
- ``MONGO_DBNAME``: MongoDB database name, default is ``rolabesti``.
- ``MONGO_COLNAME``: MongoDB collection name, default is ``tracks``.

Before running the application, locating the mp3 files in ``MUSIC_DIR`` is enough. Besides, the searching results become more accurate when the track path has one of following patterns.

- ``MUSIC_DIR/Places/<place>/Genres/<genre>/Albums/<album>/[<side>/]<title>.mp3``
- ``MUSIC_DIR/Places/<place>/Genres/<genre>/<artist>/<album>/[<side>/]<title>.mp3``
- ``MUSIC_DIR/Places/<place>/Genres/<genre>/<artist>/<title>.mp3``
- ``MUSIC_DIR/Places/<place>/Genres/<genre>/`<title>.mp3``
- ``MUSIC_DIR/Places/<place>/Albums/<album>/[<side>/]<title>.mp3``
- ``MUSIC_DIR/Places/<place>/<artist>/<album>/[<side>/]<title>.mp3``
- ``MUSIC_DIR/Places/<place>/<artist>/<title>.mp3``
- ``MUSIC_DIR/Places/<place>/<title>.mp3``
- ``MUSIC_DIR/Genres/<genre>/Albums/<album>/[<side>/]<title>.mp3``
- ``MUSIC_DIR/Genres/<genre>/<artist>/<album>/[<side>/]<title>.mp3``
- ``MUSIC_DIR/Genres/<genre>/<artist>/<title>.mp3``
- ``MUSIC_DIR/Genres/<genre>/<title>.mp3``
- ``MUSIC_DIR/Artists/<artist>/<album>/[<side>/]<title>.mp3``
- ``MUSIC_DIR/Artists/<artist>/<title>.mp3``
- ``MUSIC_DIR/Albums/<album>/[<side>/]<title>.mp3``
- ``MUSIC_DIR/[some/path/]<title>.mp3``

``<place>``, ``<genre>``, ``<artist>``, ``<album>``, ``<side>`` and ``<title>`` are placeholders of any length and character. The square brackets denote optional.

The database is loaded with tracks metadata running the ``load`` subcommand.

.. code-block:: bash

    $ rolabesti load

When selecting ``vlc`` player, unique running instance configuration is recommended.

- Tools/Preferences/Interface/Playlist and Instances
    - Allow only one instance: ``checked``
    - Enqueue items into playlist in one instance mode: ``checked``

Usage
-----

.. code-block:: bash

    $ rolabesti [-h] SUBCOMMAND [ARGUMENTS]

You can check the arguments for each subcommand with:

.. code-block:: bash

    $ rolabesti SUBCOMMAND -h

Let's see a couple of examples.

To play two hours of rock music, limiting the track length to 10 minutes, with random sorting:

.. code-block:: bash

    $ rolabesti play -g rock -l 120 --max 10 -s random

To play an hour of rap music from Iceland, skipping intro and outro tracks (less than 2 minutes length), with ascending sorting:

.. code-block:: bash

    $ rolabesti play -g rap -l 60 -p Iceland --min 2 -s asc
