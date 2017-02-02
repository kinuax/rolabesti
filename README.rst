rolabesti - Music Library Manager
=================================

-  `Motivation <#motivation>`__
-  `Description <#description>`__
-  `Requirements <#requirements>`__
-  `Installation <#installation>`__
-  `Usage <#usage>`__

Motivation
----------

The main motivation is to answer a question that music fans, DJs, bartenders and melomaniacs with tons of audio files may face: 'What music do I play?' That is, 'what genre do I want now?' or 'which random songs can fill up the time I am able to listen?' are the type of questions that **rolabesti** replies.

Description
-----------

**rolabesti** is an command-line application to manage a music library, performing the following actions on mp3 files: parsing, searching, playing, enqueueing, copying, and tagging.

Requirements
------------

-  Linux environment.
-  Python 3.3+. An isolated virtual environment is very recommended. More info about virtualenv `here <https://github.com/pypa/virtualenv>`__.
-  MongoDB running instance.
-  ``libvlc`` library and ``vlc`` player.

Installation
------------

::

    pip install rolabesti

Usage
-----

::

    rolabesti [-h] SUBCOMMAND [ARGUMENTS]

You can check the arguments for each subcommand with:

::

    rolabesti SUBCOMMAND -h

Let's see a couple of examples.

To play two hours of rock music, limiting the track length to 10 minutes, with random sorting:

::

    rolabesti play -g rock -l 120 --max 10 -s random

To play an hour of rap music from Iceland, skipping intro and outro tracks (less than 2 minutes length), with ascending sorting:

::

    rolabesti play -g rap -l 60 -p Iceland --min 2 -s asc
