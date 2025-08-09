import pytest
from watch_duty_crawler.models import EpisodeSubtitle, ExtractionScript
from watch_duty_crawler.external.script_extractor_impl import ScriptExtractorImpl


@pytest.mark.asyncio
async def test_script_extractor_impl_success() -> None:
    # 正常系: extract関数がEpisodeSubtitleを返す
    code = """
def extract(work_id, count):
    return EpisodeSubtitle(work_id=work_id, episode_count=count, subtitle=f"第{count}話タイトル")
"""
    script = ExtractionScript(script=code, work_id=123)
    extractor = ScriptExtractorImpl()
    result = await extractor.extract_subtitle(script, 123, 1)
    assert isinstance(result, EpisodeSubtitle)
    assert result.work_id == 123
    assert result.subtitle == "第1話タイトル"


@pytest.mark.asyncio
async def test_script_extractor_impl_syntax_error() -> None:
    # 構文エラー
    code = "def extract(work_id, count) return 1"  # コロン抜け
    script = ExtractionScript(script=code, work_id=123)
    extractor = ScriptExtractorImpl()
    result = await extractor.extract_subtitle(script, 123, 1)
    assert result is None


@pytest.mark.asyncio
async def test_script_extractor_impl_no_extract() -> None:
    # extract関数未定義
    code = "def foo(): return 1"
    script = ExtractionScript(script=code, work_id=123)
    extractor = ScriptExtractorImpl()
    result = await extractor.extract_subtitle(script, 123, 1)
    assert result is None


@pytest.mark.asyncio
async def test_script_extractor_impl_wrong_type() -> None:
    # extract関数がEpisodeSubtitle以外を返す
    code = """
def extract(work_id, count):
    return "not subtitle object"
"""
    script = ExtractionScript(script=code, work_id=123)
    extractor = ScriptExtractorImpl()
    result = await extractor.extract_subtitle(script, 123, 1)
    assert result is None
