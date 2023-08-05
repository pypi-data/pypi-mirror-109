from dataclasses import dataclass
from px_settings.contrib.django import settings as s


__all__ = 'Settings',


@s('WCD_GEO_DB')
@dataclass
class Settings:
    DB_NAME: str = 'default'
