from typing import Optional, Dict, Any
from watch_duty_crawler.models import EpisodeSubtitle, ExtractionScript
from watch_duty_crawler.usecase.subtitle_fetcher import ScriptExtractor


class ScriptExtractorImpl(ScriptExtractor):
    """ExtractionScriptをPythonコードとして実行する実装例"""

    async def extract_subtitle(
        self, script: ExtractionScript, work_id: int, count: int
    ) -> Optional[EpisodeSubtitle]:
        # ExtractionScriptがPythonコード文字列である前提
        code = getattr(script, "script", str(script))
        # 構文チェック
        try:
            compile(code, "<extraction_script>", "exec")
        except SyntaxError as e:
            print(f"Script syntax error: {e}")
            return None

        local_vars: Dict[str, Any] = {}
        exec(code, {"EpisodeSubtitle": EpisodeSubtitle}, local_vars)
        extract_func = local_vars.get("extract")
        if not extract_func:
            print("No 'extract' function found in script")
            return None
        try:
            result = extract_func(work_id, count)
        except Exception as e:
            print(f"Script execution error: {e}")
            return None
        if not isinstance(result, EpisodeSubtitle):
            print("Result is not EpisodeSubtitle")
            return None
        return result
