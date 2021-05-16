"""Application configuration."""
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="VH7",
    settings_files=['settings.toml', '.secrets.toml'],
)
