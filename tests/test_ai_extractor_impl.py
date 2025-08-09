import os
import pytest
from watch_duty_crawler.external.ai_extractor_impl import AIExtractorImpl
from watch_duty_crawler.models import EpisodeSubtitle, ExtractionScript


@pytest.mark.asyncio
async def test_ai_extractor_impl_no_api_key() -> None:
    # APIキー未設定時はNoneが返る
    if os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("APIキーが設定されている場合はスキップ")
    extractor = AIExtractorImpl()
    subtitle, script = await extractor.extract_subtitle(1, 1)
    assert subtitle is None
    assert script is None


@pytest.mark.asyncio
async def test_ai_extractor_impl_success() -> None:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        pytest.skip("APIキーが未設定のためスキップ")
    extractor = AIExtractorImpl()
    title = "薫る花は凛と咲く"
    count = 5
    url = "https://kaoruhana-anime.com"
    subtitle, script = await extractor.extract_subtitle(title, count, url)
    assert isinstance(subtitle, EpisodeSubtitle)
    assert isinstance(script, ExtractionScript)
    assert "はじまりの予感" in subtitle.subtitle
