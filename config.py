"""Application configuration."""
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="QUARK",
    settings_files=['settings.toml', '.secrets.toml'],
)
