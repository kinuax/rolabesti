from functools import lru_cache

from pydantic import ValidationError
from tomlkit import dumps

from .settings import Settings, toml_file


@lru_cache
def get_settings() -> Settings:
    """Return the current settings."""
    try:
        return Settings()
    except ValidationError:
        # Recover if configuration file is incorrectly edited.
        reset_settings()
        return Settings()


def reset_settings() -> None:
    """Empty configuration file."""
    toml_file.write_text("")


def store_settings(settings: Settings) -> None:
    """Store settings in the configuration file."""
    toml_file.write_text(dumps(settings.model_dump(exclude_unset=True)))
