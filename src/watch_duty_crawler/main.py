import uvicorn
from watch_duty_crawler.web_server import (
    create_app,
    SubtitleFetcher,
    MockAIExtractor,
    MockScriptExtractor,
    MockScriptRepository,
)


def main() -> None:
    # モック実装でDI
    fetcher = SubtitleFetcher(
        script_repository=MockScriptRepository(),
        ai_extractor=MockAIExtractor(),
        script_extractor=MockScriptExtractor(),
    )
    app = create_app(fetcher)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
