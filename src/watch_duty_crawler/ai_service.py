"""AI service interface for subtitle extraction."""

from .models import EpisodeSubtitle, Work
from .usecase import Extractor


class AISubtitleExtractor(Extractor):
    """Abstract interface for AI-based subtitle extraction."""

    async def extract_subtitle(self, anime_info: Work) -> EpisodeSubtitle:
        """Extract episode subtitles from anime information.

        Args:
            anime_info: Anime title and official URL

        Returns:
            Collection of episode subtitles

        Raises:
            AIServiceError: If the AI service fails
        """
        raise NotImplementedError("Subclasses must implement extract_subtitles method")


class AIServiceError(Exception):
    """Exception raised when AI service fails."""

    pass
