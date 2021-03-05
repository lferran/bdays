import copy
import json

from pydantic import BaseModel

_cached_settings = None


default_config = {}


class Settings(BaseModel):
    dsn: str


def load_settings(config_file: str) -> Settings:
    global _cached_settings

    with open(config_file, "r") as f:
        config_file_options = json.loads(f.read())

    default = copy.deepcopy(default_config)
    default.update(config_file_options)

    settings = Settings.parse_obj(default)

    _cached_settings = settings


def get_settings() -> Settings:
    return _cached_settings
