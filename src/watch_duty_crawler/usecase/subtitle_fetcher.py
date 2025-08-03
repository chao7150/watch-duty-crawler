import asyncio
from abc import ABC, abstractmethod
from watch_duty_crawler.models import EpisodeSubtitle, Work


class Extractor(ABC):
    """Interface for subtitle extraction services."""

    @abstractmethod
    async def extract_subtitles(self, anime_info: Work) -> list[EpisodeSubtitle]:
        """Extract episode subtitles from anime information.

        Args:
            anime_info: Anime title and official URL

        Returns:
            List of episode subtitles
        """
        pass


class SubtitleFetcher:
    """Fetches episode subtitles using subtitle extraction service."""

    def __init__(self, extractor: Extractor):
        self.extractor = extractor

    async def fetch_subtitles_batch(
        self, anime_list: list[Work]
    ) -> list[list[EpisodeSubtitle]]:
        tasks = [self._fetch_single_anime(anime_info) for anime_info in anime_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        subtitle_list: list[list[EpisodeSubtitle]] = []
        for i, result in enumerate(results):
            anime_info = anime_list[i]
            if isinstance(result, Exception):
                print(f"Failed to fetch subtitles for {anime_info.title}: {result}")
                continue
            assert isinstance(result, list)
            subtitle_list.append(result)
        return subtitle_list

    async def _fetch_single_anime(self, anime_info: Work) -> list[EpisodeSubtitle]:
        print(f"Fetching subtitles for: {anime_info.title}")
        return await self.extractor.extract_subtitles(anime_info)
