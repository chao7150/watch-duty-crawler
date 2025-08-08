"""Simple models for subtitle fetching."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Work:
    """Basic anime information."""

    id: int
    title: str
    official_url: str


@dataclass
class EpisodeSubtitle:
    """Episode subtitle information."""

    work_id: int
    episode_count: int
    subtitle: str
    additional_info: Optional[str] = None
    air_date: Optional[str] = None


@dataclass
class ExtractionScript:
    script: str
    work_id: int
