"""
CLI application to manage collections of mp3 tracks and to support parsing ID3 tags
and file paths, loading database, searching, playing, copying, and tagging.
"""

from importlib import metadata

__version__ = metadata.version("rolabesti")
__description__ = metadata.metadata("rolabesti")["Summary"]
