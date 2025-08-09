import json
from typing import Any, Dict, List, Optional
import httpx


class PlaywrightHTTPClient:
    """Playwright MCP HTTPサーバーとの通信を管理するクライアント"""

    def __init__(self, base_url: str = "http://localhost:8082") -> None:
        self.base_url = base_url
        self.mcp_url = f"{base_url}/mcp"
        self._tools: List[Dict[str, Any]] = []
        self.session_id: Optional[str] = None

    async def connect(self) -> bool:
        """Playwright MCP HTTPサーバーに接続"""
        try:
            async with httpx.AsyncClient() as client:
                # STEP 1: MCP初期化してセッションIDを取得
                response = await client.post(
                    self.mcp_url,
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2025-03-26",
                            "capabilities": {"roots": {}, "sampling": {}},
                            "clientInfo": {
                                "name": "watch-duty-crawler",
                                "version": "1.0.0",
                            },
                        },
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream",
                    },
                    timeout=30.0,
                )

                if response.status_code != 200:
                    print(f"MCP初期化失敗: {response.status_code}")
                    return False

                # セッションIDを取得
                self.session_id = response.headers.get("mcp-session-id")
                if not self.session_id:
                    print("mcp-session-idヘッダーが見つかりません")
                    return False

                print(f"MCP セッションID取得: {self.session_id}")

                # STEP 2: initialized通知を送信
                await client.post(
                    self.mcp_url,
                    json={"jsonrpc": "2.0", "method": "initialized", "params": {}},
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream",
                        "mcp-session-id": self.session_id,
                    },
                    timeout=30.0,
                )

                # STEP 3: 利用可能なツールを取得
                tools_response = await client.post(
                    self.mcp_url,
                    json={
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/list",
                        "params": {},
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream",
                        "mcp-session-id": self.session_id,
                    },
                    timeout=30.0,
                )

                if tools_response.status_code == 200:
                    tools_text = tools_response.text
                    if tools_text.startswith("event: message\ndata: "):
                        json_data = tools_text.split("data: ")[1].strip()
                        tools_result = json.loads(json_data)
                    else:
                        tools_result = tools_response.json()

                    if "result" in tools_result and "tools" in tools_result["result"]:
                        self._tools = [
                            self._convert_tool_format(tool)
                            for tool in tools_result["result"]["tools"]
                        ]
                        print(
                            f"利用可能なツール: {[tool['function']['name'] for tool in self._tools]}"
                        )

                return True

        except Exception as e:
            print(f"Playwright MCP HTTPサーバーへの接続失敗: {e}")
            return False

    def _convert_tool_format(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """MCPツール定義をOpenAI互換の形式に変換"""
        return {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool.get("inputSchema", {}),
            },
        }

    async def get_tools(self) -> List[Dict[str, Any]]:
        """利用可能なツールリストを取得"""
        return self._tools

    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Optional[str]:
        """MCPツールを実行"""
        if not self.session_id:
            print("セッションIDが設定されていません")
            return None

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.mcp_url,
                    json={
                        "jsonrpc": "2.0",
                        "id": 3,
                        "method": "tools/call",
                        "params": {"name": tool_name, "arguments": args},
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream",
                        "mcp-session-id": self.session_id,
                    },
                    timeout=60.0,
                )

                if response.status_code != 200:
                    print(f"ツール {tool_name} 実行失敗: {response.status_code}")
                    return None

                # SSE形式のレスポンスを解析
                response_text = response.text
                if response_text.startswith("event: message\ndata: "):
                    json_data = response_text.split("data: ")[1].strip()
                    result = json.loads(json_data)
                else:
                    result = response.json()
                if "result" in result and "content" in result["result"]:
                    content = result["result"]["content"]
                    if isinstance(content, list) and len(content) > 0:
                        first_item = content[0]
                        if isinstance(first_item, dict) and "text" in first_item:
                            return str(first_item["text"])
                    elif isinstance(content, str):
                        return content

                return None

        except Exception as e:
            print(f"ツール {tool_name} の実行エラー: {e}")
            return None


# グローバルなHTTPクライアントインスタンス
_http_client: Optional[PlaywrightHTTPClient] = None


async def get_mcp_client() -> Optional[PlaywrightHTTPClient]:
    """MCP HTTPクライアントのインスタンスを取得"""
    global _http_client

    if not _http_client:
        _http_client = PlaywrightHTTPClient()
        if not await _http_client.connect():
            return None

    return _http_client
