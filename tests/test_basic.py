"""Test the basic subtitle fetching functionality."""

import asyncio
import pytest

from watch_duty_crawler.models import Work, EpisodeSubtitle
from watch_duty_crawler.ai_service import AISubtitleExtractor
from watch_duty_crawler.usecase import SubtitleFetcher


class MockAIExtractor(AISubtitleExtractor):
    """Mock AI extractor for testing."""

    async def extract_subtitles(self, anime_info: Work) -> list[EpisodeSubtitle]:
        """Mock implementation that returns dummy data."""
        await asyncio.sleep(0.1)
        return [
            EpisodeSubtitle(
                work_id=getattr(anime_info, "id", 1),
                episode_count=1,
                subtitle="第1話のタイトル",
            ),
            EpisodeSubtitle(
                work_id=getattr(anime_info, "id", 1),
                episode_count=2,
                subtitle="第2話のタイトル",
            ),
            EpisodeSubtitle(
                work_id=getattr(anime_info, "id", 1),
                episode_count=3,
                subtitle="第3話のタイトル",
            ),
        ]


@pytest.mark.asyncio
async def test_basic_functionality() -> None:
    """Test basic subtitle fetching functionality."""
    # Setup
    mock_ai = MockAIExtractor()
    fetcher = SubtitleFetcher(mock_ai)

    # Test data
    anime_list = [
        Work(id=1, title="進撃の巨人", official_url="https://shingeki.tv/"),
        Work(id=2, title="呪術廻戦", official_url="https://jujutsukaisen.jp/"),
    ]

    # Execute
    results = await fetcher.fetch_subtitles_batch(anime_list)

    # Verify
    print(f"Successfully fetched subtitles for {len(results)} anime:")
    for i, subtitles in enumerate(results):
        print(f"\n{anime_list[i].title}:")
        for episode in subtitles:
            print(f"  Episode {episode.episode_count}: {episode.subtitle}")


if __name__ == "__main__":
    asyncio.run(test_basic_functionality())
