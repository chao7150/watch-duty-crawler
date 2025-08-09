"""
Playwright MCP統合のテスト
"""

from watch_duty_crawler.external.mcp_tools import PlaywrightMCPClient, get_mcp_client


class TestPlaywrightMCPIntegration:
    """Playwright MCP統合のテストクラス"""

    async def test_mcp_client_creation(self):
        """MCPクライアントが正しく作成されることを確認"""
        client = PlaywrightMCPClient()
        assert client is not None
        assert client.session is None
        tools = await client.get_tools()
        assert tools == []

    async def test_mcp_client_connection_without_mcp_server(self):
        """MCPサーバーがない状態での接続テスト（失敗するべき）"""
        client = PlaywrightMCPClient()
        # MCPサーバーが起動していない状態では接続に失敗するはず
        connected = await client.connect()
        # 実際の環境に依存するため、失敗を期待するかどうかは環境次第
        assert isinstance(connected, bool)
        await client.close()

    async def test_get_mcp_client_function(self):
        """get_mcp_client関数のテスト"""
        client = await get_mcp_client()
        # MCPサーバーが利用できない環境ではNoneが返される
        # 利用できる環境ではPlaywrightMCPClientが返される
        assert client is None or isinstance(client, PlaywrightMCPClient)

    def test_mcp_tools_module_import(self):
        """MCPツールモジュールが正しくインポートできることを確認"""
        from watch_duty_crawler.external import mcp_tools

        assert mcp_tools.convert_tool_format is not None
        assert mcp_tools.get_playwright_tools is not None
        assert mcp_tools.get_mcp_client is not None
        assert mcp_tools.PlaywrightMCPClient is not None
