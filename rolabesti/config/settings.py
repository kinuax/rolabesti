from enum import Enum
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


max_overlap_length = 30
tinydb_directory = user_data_path(__app_name__)
tinydb_file = tinydb_directory / "tracks.json"
toml_file = user_config_path(__app_name__) / "config.toml"


class Databases(str, Enum):
    # mongodb = "mongodb"
    tinydb = "tinydb"


class Settings(BaseSettings):
    max_track_length: NonNegativeInt = 10
    min_track_length: NonNegativeInt = 0
    max_tracklist_length: NonNegativeInt = 60
    sorting: Sortings = Sortings.random
    overlap_length: int = Field(3, ge=0, le=max_overlap_length)
    music_directory: DirectoryPath = user_music_path()
    copy_directory: DirectoryPath = user_documents_path()
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
