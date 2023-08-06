from dataclasses import dataclass, field
from typing import Sequence, Tuple
from django.conf import settings as django_settings
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings'


@s('PXD_LINGUA')
@dataclass
class Settings:
    LANGUAGE_CODE: str = field(
        default_factory=lambda: django_settings.LANGUAGE_CODE
    )
    LANGUAGES: Sequence[Tuple[str, str]] = field(
        default_factory=lambda: django_settings.LANGUAGES
    )


settings = Settings()
