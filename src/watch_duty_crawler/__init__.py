"""Watch Duty Crawler package.

A subtitle fetching system for anime episodes.
"""

__version__ = "0.1.0"
__author__ = "chao7150"

# Core components
from .usecase import SubtitleFetcher
from .models import Work, EpisodeSubtitle
from .ai_service import AISubtitleExtractor, AIServiceError

__all__ = [
    "SubtitleFetcher",
    "Work",
    "EpisodeSubtitle",
    "AISubtitleExtractor",
    "AIServiceError",
    "__version__",
    "__author__",
]
