import uvicorn
from watch_duty_crawler.web_server import (
    create_app,
    SubtitleFetcher,
    MockAIExtractor,
    MockScriptRepository,
)
from watch_duty_crawler.external.script_extractor_impl import ScriptExtractorImpl


def main() -> None:
    fetcher = SubtitleFetcher(
        script_repository=MockScriptRepository(),
        ai_extractor=MockAIExtractor(),
        script_extractor=ScriptExtractorImpl(),
    )
    app = create_app(fetcher)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
