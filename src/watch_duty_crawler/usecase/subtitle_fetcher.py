import asyncio
from abc import ABC, abstractmethod
from typing import Optional
from watch_duty_crawler.models import EpisodeSubtitle, ExtractionScript, Work


class ScriptExtractor(ABC):
    """Interface for subtitle extraction services."""

    @abstractmethod
    async def extract_subtitle(
        self, script: ExtractionScript, work_id: int, count: int
    ) -> Optional[EpisodeSubtitle]:
        """Extract episode subtitle from work information and episode count.

        Args:
            anime_info: Anime title and official URL

        Returns:
            Episode subtitle
        """
        pass


class AIExtractor(ABC):
    """Interface for AI-based subtitle extraction."""

    @abstractmethod
    async def extract_subtitle(
        self, title: str, count: int, url: Optional[str] = None
    ) -> tuple[Optional[EpisodeSubtitle], Optional[ExtractionScript]]:
        """Extract episode subtitles from anime information.

        Args:
            work: Anime title and official URL
            count: Number of episodes to fetch

        Returns:
            Episode subtitle and generated script
        """
        pass


class ScriptRepository(ABC):
    @abstractmethod
    async def save(self, script: ExtractionScript) -> None:
        """Save the extraction script."""
        pass

    @abstractmethod
    async def load(self, work_id: int) -> Optional[ExtractionScript]:
        """Load the extraction script for a given work ID and episode count.

        Args:
            work_id: ID of the work
            episode_count: Number of episodes

        Returns:
            Optional extraction script if found, otherwise None
        """
        pass


class SubtitleFetcher:
    """Fetches episode subtitles using subtitle extraction service."""

    def __init__(
        self,
        script_repository: ScriptRepository,
        ai_extractor: AIExtractor,
        script_extractor: ScriptExtractor,
    ):
        self.script_repository = script_repository
        self.ai_extractor = ai_extractor
        self.script_extractor = script_extractor

    async def fetch_single_anime(
        self, work: Work, count: int
    ) -> Optional[EpisodeSubtitle]:
        script = await self.script_repository.load(work.id)
        if script:
            r = await self.script_extractor.extract_subtitle(script, work.id, count)
            if r:
                return r

        (r, s) = await self.ai_extractor.extract_subtitle(
            work.title, count, work.official_url
        )
        if s:
            asyncio.create_task(self.script_repository.save(s))
        return r
