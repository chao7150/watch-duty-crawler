"""Test the basic subtitle fetching functionality."""

import asyncio
from typing import Optional
import pytest

from watch_duty_crawler.models import Work, EpisodeSubtitle, ExtractionScript
from watch_duty_crawler.usecase.subtitle_fetcher import (
    SubtitleFetcher,
    AIExtractor,
    ScriptExtractor,
    ScriptRepository,
)


class MockAIExtractor(AIExtractor):
    async def extract_subtitle(
        self, title: str, count: int, url: Optional[str] = None
    ) -> tuple[Optional[EpisodeSubtitle], Optional[ExtractionScript]]:
        await asyncio.sleep(0.1)
        return (
            EpisodeSubtitle(
                episode_count=count,
                subtitle=f"第{count}話のタイトル",
            ),
            ExtractionScript(script="print('dummy')", title=title),
        )


class MockScriptExtractor(ScriptExtractor):
    async def extract_subtitle(
        self, script: ExtractionScript, work_id: int, count: int
    ) -> EpisodeSubtitle | None:
        return None


class MockScriptRepository(ScriptRepository):
    async def save(self, script: ExtractionScript) -> None:
        pass

    async def load(self, work_id: int) -> ExtractionScript | None:
        return None


@pytest.mark.asyncio
async def test_single_anime() -> None:
    mock_ai = MockAIExtractor()
    mock_script = MockScriptExtractor()
    mock_repo = MockScriptRepository()
    fetcher = SubtitleFetcher(
        script_repository=mock_repo,
        ai_extractor=mock_ai,
        script_extractor=mock_script,
    )
    work = Work(id=1, title="進撃の巨人", official_url="https://shingeki.tv/")
    result = await fetcher.fetch_single_anime(work, 1)
    assert result is not None
    assert result.episode_count == 1
    assert result.subtitle == "第1話のタイトル"
