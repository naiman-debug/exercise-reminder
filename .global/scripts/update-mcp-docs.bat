@echo off
echo ========================================
echo   MCP & Plugin 文档更新工具
echo ========================================
echo.
echo 正在扫描 MCP 服务器...
echo.

cd /d "%~dp0"
node update-mcp-docs.js

echo.
echo ========================================
echo   更新完成！
echo ========================================
echo.
pause
