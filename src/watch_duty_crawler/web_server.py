# pyright: reportUnusedFunction=false
import asyncio
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    ) -> Optional[EpisodeSubtitle]:
        return None


class MockScriptRepository(ScriptRepository):
    async def save(self, script: ExtractionScript) -> None:
        pass

    async def load(self, work_id: int) -> Optional[ExtractionScript]:
        return None


class FetchRequest(BaseModel):
    work_id: int
    count: int
    title: str
    official_url: str


def create_app(fetcher: SubtitleFetcher) -> FastAPI:
    app = FastAPI()

    @app.post("/fetch_subtitle")
    async def fetch_subtitle(req: FetchRequest) -> Dict[str, Any]:
        work = Work(
            id=req.work_id,
            title=req.title,
            official_url=req.official_url,
        )
        result = await fetcher.fetch_single_anime(work, req.count)
        if result is None:
            raise HTTPException(status_code=404, detail="Subtitle not found")
        return {
            "episode_count": result.episode_count,
            "subtitle": result.subtitle,
        }

    return app


if __name__ == "__main__":
    # web_server.py単体実行時はモック実装でAPIサーバー起動
    fetcher = SubtitleFetcher(
        script_repository=MockScriptRepository(),
        ai_extractor=MockAIExtractor(),
        script_extractor=MockScriptExtractor(),
    )
    app = create_app(fetcher)
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
