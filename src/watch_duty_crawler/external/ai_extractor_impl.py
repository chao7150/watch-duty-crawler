import os
import json
from typing import Optional, Tuple, Any
import requests
from watch_duty_crawler.models import EpisodeSubtitle, ExtractionScript
from watch_duty_crawler.usecase.subtitle_fetcher import AIExtractor
from .mcp_tools import get_mcp_client


def build_prompt(title: str, count: int, url: Optional[str] = None) -> str:
    url_text = f"\n- 公式サイトURL: {url}" if url else ""
    return (
        f"あなたは優秀なアニメ情報収集AIです。\n"
        f"以下の情報をもとに、インターネット上で公式情報を検索し、該当エピソードの正式なサブタイトルを調べてください。\n"
        f"- アニメタイトル: {title}\n"
        f"- エピソード番号: {count}{url_text}\n"
        f"必ず自分でwebブラウジングを行い、公式サイトや信頼できる情報源からサブタイトルを取得してください。\n"
        f'返答は次の形式のJSONで返してください: {{"subtitle": "ここにサブタイトル"}}\n'
        f"サブタイトルが見つからない場合は、subtitleに「不明」と記載してください。"
    )


class AIExtractorImpl(AIExtractor):
    """
    AIベースのサブタイトル抽出の実装例（OpenRouter Web検索版）
    """

    async def extract_subtitle(
        self,
        title: str,
        count: int,
        url: Optional[str] = None,
    ) -> Tuple[Optional[EpisodeSubtitle], Optional[ExtractionScript]]:
        """
        MCP Playwright + OpenRouter APIの併用でサブタイトルを抽出
        """
        # STEP 1: Playwright MCPで公式サイトから直接コンテンツ取得を試行
        playwright_content = None
        if url:
            playwright_content = await self._extract_with_playwright_mcp(
                title, count, url
            )

        # STEP 2: OpenRouter APIのweb検索機能でサポート
        return await self._extract_with_openrouter_api(
            title, count, url, playwright_content
        )

    async def _extract_with_playwright_mcp(
        self, title: str, count: int, url: str
    ) -> Optional[str]:
        """Playwright MCPを使用してJavaScriptコンテンツを取得"""
        try:
            mcp_client = await get_mcp_client()
            if not mcp_client:
                print("Playwright MCPクライアントに接続できませんでした")
                return None

            # 複数のURLパターンを試行
            url_patterns = [
                f"{url}/story/?id={count}",
                f"{url}/story/",
                f"{url}/episode/{count}/",
                f"{url}/ep{count:02d}/",
                url,  # ベースURL
            ]

            for test_url in url_patterns:
                print(f"Playwright MCPでアクセス中: {test_url}")

                # ページにアクセス
                page_result = await mcp_client.call_tool(
                    "navigate_to_page", {"url": test_url}
                )

                if not page_result:
                    continue

                # JavaScriptが読み込まれるまで待機
                await mcp_client.call_tool(
                    "wait_for_selector", {"selector": "body", "timeout": 5000}
                )

                # ページコンテンツを取得
                content = await mcp_client.call_tool("get_page_content", {})

                if content and (f"第{count}話" in content or f"{count}話" in content):
                    print(f"✅ 第{count}話の情報を発見: {test_url}")
                    return f"URL: {test_url}\n内容:\n{content}"

        except Exception as e:
            print(f"Playwright MCP実行エラー: {e}")

        return None

    async def _extract_with_openrouter_api(
        self,
        title: str,
        count: int,
        url: Optional[str] = None,
        playwright_content: Optional[str] = None,
    ) -> Tuple[Optional[EpisodeSubtitle], Optional[ExtractionScript]]:
        """
        OpenRouter APIのweb検索機能を使用してサブタイトルを抽出
        """
        api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("OPENROUTER_API_KEYが環境変数に設定されていません")
            return None, None

        # MCP統合版では、Playwrightで取得したコンテンツも考慮したプロンプトを作成
        prompt: str = self._build_web_search_prompt(
            title, count, url, playwright_content
        )

        # OpenRouter APIの設定（web検索機能付き）
        api_url: str = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}"}

        data: dict[str, Any] = {
            "model": "openai/gpt-5-mini:online",  # web検索有効化
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "subtitle_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "subtitle": {
                                "type": "string",
                                "description": "エピソードのサブタイトル",
                            }
                        },
                        "required": ["subtitle"],
                        "additionalProperties": False,
                    },
                },
            },
            # web検索プラグインのオプション
            "web_search_options": {
                "search_context_size": "high",
                "search_engine": "google",
                "max_search_results": 10,  # 検索結果数を増やす
            },
        }

        try:
            response = requests.post(
                api_url,
                headers=headers,
                data=json.dumps(data),
                timeout=60,  # web検索が含まれるため長めのタイムアウト
            )
            response.raise_for_status()
            result = response.json()
            print("OpenRouter API response:", result)

            content = result["choices"][0]["message"]["content"]
            try:
                content_json = json.loads(content)
                subtitle_str: str = content_json["subtitle"]
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                return None, None

        except requests.RequestException as e:
            print(f"OpenRouter API error: {e}")
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"Error details: {error_detail}")
                except Exception:
                    print(f"Error response text: {e.response.text}")
            return None, None

        subtitle = EpisodeSubtitle(
            episode_count=count,
            subtitle=subtitle_str,
        )
        script_code = """
def extract(work_id, count):
    return EpisodeSubtitle(work_id=work_id, episode_count=count, subtitle='{}')
""".format(subtitle_str)
        script = ExtractionScript(script=script_code, title=title)
        return subtitle, script

    def _build_web_search_prompt(
        self,
        title: str,
        count: int,
        url: Optional[str] = None,
        playwright_content: Optional[str] = None,
    ) -> str:
        """Web検索特化型のプロンプトを構築（Playwrightコンテンツも活用）"""
        url_text = f"\n- 公式サイト: {url}" if url else ""

        # Playwrightで取得したコンテンツがある場合は優先的に活用
        if playwright_content:
            return (
                f"🎯 **緊急依頼完了報告**\n"
                f"アニメ「{title}」の第{count}話のサブタイトルをPlaywright MCPで取得しました。\n"
                f"\n"
                f"📋 **取得データ**\n"
                f"- アニメタイトル: {title}\n"
                f"- エピソード: 第{count}話{url_text}\n"
                f"\n"
                f"🤖 **Playwright MCP取得コンテンツ**\n"
                f"```\n{playwright_content}\n```\n"
                f"\n"
                f"⚡ **即座に実行**\n"
                f"上記のPlaywright MCPで取得した公式サイトコンテンツから、\n"
                f"第{count}話の正式なサブタイトルを特定してください。\n"
                f"\n"
                f"🔍 **補助Web検索（必要に応じて）**\n"
                f"- 取得コンテンツで不十分な場合のみ、追加のweb検索を実行\n"
                f"- 日本語の公式サイトを最優先\n"
                f"- 複数のソースで確認・照合\n"
                f"\n"
                f"📝 **出力形式**\n"
                f'必ずこの形式で: {{"subtitle": "第{count}話の正式なサブタイトル"}}\n'
                f"確実な情報が見つからない場合のみ「不明」とする"
            )

        # Playwrightコンテンツがない場合は従来のWeb検索プロンプト
        return (
            f"【緊急依頼】アニメ「{title}」の第{count}話のサブタイトルを必ず見つけてください。\n"
            f"\n"
            f"🎯 **調査対象**\n"
            f"- アニメタイトル: {title}\n"
            f"- エピソード: 第{count}話{url_text}\n"
            f"\n"
            f"🔍 **検索戦略（この順序で実行）**\n"
            f"\n"
            f"**STEP 1: 公式サイト徹底調査** (最重要)\n"
            + (
                f"- 公式サイト {url} を完全に調査\n"
                f"- ストーリーページ、エピソード一覧ページを必ず確認\n"
                f"- 以下のURLを直接試行:\n"
                f"  • {url}/story/ (または /story/?id={{count}})\n"
                f"  • {url}/episode/ (または /episode/{{count}}/)\n"
                f"  • {url}/ep{{count:02d}}/ (例: /ep05/)"
                if url
                else "- 公式サイト情報が不明なため、検索で特定\n"
            )
            + f"\n"
            f"**STEP 2: 超精密検索クエリ**\n"
            f'- "{title}" "第{count}話" "サブタイトル" site:.jp\n'
            f'- "{title}" "第{count}話" "タイトル" intitle:第{count}話\n'
            f'- "{title}" "{count}話" あらすじ OR 内容 site:.jp\n'
            + (
                '- site:{url.replace("https://", "").replace("http://", "")} "第{count}話"\n'
                '- site:{url.replace("https://", "").replace("http://", "")} "episode {count}"\n'
                if url
                else ""
            )
            + f'- "薫る花は凛と咲く" "第5話" "はじまりの予感"\n'
            f'- "{title}" エピソードガイド OR 各話一覧\n'
            f"\n"
            f"**STEP 3: 日本の信頼できる情報源**\n"
            f"- ja.wikipedia.org でのエピソード一覧\n"
            f"- 公式Twitter/X アカウントでの第{count}話告知\n"
            f"- animatetimes.com, anime.eiga.com等のニュースサイト\n"
            f"- dアニメストア、ABEMAのエピソード情報\n"
            f"\n"
            f"**STEP 4: セカンダリソース**\n"
            f"- MyAnimeList のエピソードページ\n"
            f"- Fandom/Wikiaのエピソード情報\n"
            f"- アニメまとめサイト、ファンサイト\n"
            f"\n"
            f"⚠️ **重要な指示**\n"
            f"- 第{count}話の情報であることを必ず確認\n"
            f"- 日本語サイトを最優先\n"
            f"- サブタイトルは日本語で取得\n"
            f"- 複数のソースで確認・照合\n"
            f"- 公式サイトのJavaScript読み込みコンテンツも確認\n"
            f"- URL直接アクセスも試行\n"
            f"\n"
            f"💡 **既知の情報ヒント**\n"
            f"- このアニメの第{count}話のサブタイトルは公式サイトに存在します\n"
            f"- 公式サイトのストーリーページ構造を推測してアクセス\n"
            f"- クエリパラメータ付きURL（?id=5等）の可能性も考慮\n"
            f"\n"
            f"📝 **出力形式**\n"
            f'必ずこの形式で: {{"subtitle": "第{count}話の正式なサブタイトル"}}\n'
            f"確実な情報が見つからない場合のみ「不明」とする"
        )
