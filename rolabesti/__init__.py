from importlib import metadata


__app_name__ = "rolabesti"
__description__ = metadata.metadata(__app_name__)["Summary"]
__version__ = metadata.version(__app_name__)
