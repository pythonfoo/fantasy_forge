from pathlib import Path
from typing import Any

import huepy
from fluent.runtime import FluentLocalization, FluentResourceLoader
from fluent.runtime.types import FluentNone

from fantasy_forge.utils import LOCALE_FOLDER

DEFAULT_LOCALE: str = "en"


def highlight_interactive(text: Any) -> FluentNone:
    """INTER() for the localization"""
    return FluentNone(huepy.bold(huepy.green(str(text))))


def highlight_number(text: Any) -> FluentNone:
    """NUM() for the localization"""
    return FluentNone(huepy.bold(huepy.orange(str(text))))


def check_exists(obj: Any):
    """EXISTS() for the localization"""
    return str(not isinstance(obj, FluentNone)).lower()


def get_fluent_locale(locale: str = DEFAULT_LOCALE) -> FluentLocalization:
    locale_path: Path = LOCALE_FOLDER / locale
    fluent_loader: FluentResourceLoader = FluentResourceLoader(locale_path)
    l10n = FluentLocalization(
        locales=locale, resource_ids=["main.ftl"], resource_loader=fluent_loader
    )
    return l10n
