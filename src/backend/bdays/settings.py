from pydantic import BaseModel
import json

_cached_settings = None


default_config = {}

class Settings(BaseModel):
    dsn: str


def load_settings(config_file: str) -> Settings:
    global _cached_settings

    cli_options = parse_arguments()

    with open(config_file, "r") as f:
        config_file_options = json.loads(f.read())

    default = copy.deepcopy(default_options)
    default.update(config_file_options)
    default.update(cli_options)

    settings =  Settings.parse_obj(default)

    _cached_settings = settings


def get_settings() -> Settings:
    return _cached_settings
