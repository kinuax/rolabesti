from enum import Enum
from pathlib import Path
from typing import Type

from platformdirs import user_config_path, user_data_path, user_music_path, user_documents_path
from pydantic import DirectoryPath, Field, NonNegativeInt, field_serializer
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from rolabesti import __app_name__
from rolabesti.models import Sortings


def create_directories(directories: list[Path]) -> None:
    """Ensure directories are created."""
    for path in directories:
        if not path.exists():
            path.mkdir(parents=True)
            print(f"created {path}")  # TODO remove


max_overlap_length = 30
copy_path = user_documents_path()
music_path = user_music_path()
tinydb_path = user_data_path(__app_name__)
toml_path = user_config_path(__app_name__)
create_directories([copy_path, music_path, tinydb_path, toml_path])
tinydb_file = tinydb_path / "tracks.json"
toml_file = toml_path / "config.toml"


class Databases(str, Enum):
    # mongodb = "mongodb"
    tinydb = "tinydb"


class Settings(BaseSettings):
    max_track_length: NonNegativeInt = 10
    min_track_length: NonNegativeInt = 0
    max_tracklist_length: NonNegativeInt = 60
    sorting: Sortings = Sortings.random
    overlap_length: int = Field(3, ge=0, le=max_overlap_length)
    music_directory: DirectoryPath = music_path
    copy_directory: DirectoryPath = copy_path
    database: Databases = Databases.tinydb
    model_config = SettingsConfigDict(
        toml_file=toml_file,
        use_enum_values=True,
        validate_assignment=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)

    @field_serializer("music_directory")
    def serialize_music_directory(self, path: DirectoryPath, _info):
        return str(path)

    @field_serializer("copy_directory")
    def serialize_copy_directory(self, path: DirectoryPath, _info):
        return str(path)
