# MCP 服务器配置文档

> **更新日期**：2026-01-19
> **用途**：记录所有已安装的 MCP 服务器及其状态
> **总计**：23 个服务器

---

## 一、已安装并连接成功 (18个)

### godot 🎮
- **状态**：✓ 已连接
- **命令**：`node F:\claude-code\tools\godot-mcp\build\index.js`
- **说明**：Godot 游戏引擎集成，支持场景管理、节点操作、项目运行
- **环境变量**：
  - `GODOT_PATH=F:\godot\Godot_v4.5.1-stable_win64.exe`
  - `DEBUG=false`
  - `READ_ONLY_MODE=false`
- **主要功能**：
  - 启动/控制 Godot 编辑器
  - 创建和修改场景
  - 添加/编辑/删除节点
  - 运行项目并捕获调试输出
  - 项目结构分析

### web-search-prime
- **状态**：✓ 已连接
- **命令**：`https://api.z.ai/api/mcp/web_search_prime/mcp (HTTP)`

### zai-mcp-server
- **状态**：✓ 已连接
- **命令**：`npx -y @z_ai/mcp-server`

### web-reader
- **状态**：✓ 已连接
- **命令**：`https://api.z.ai/api/mcp/web_reader/mcp (HTTP)`

### zread
- **状态**：✓ 已连接
- **命令**：`https://api.z.ai/api/mcp/zread/mcp (HTTP)`

### filesystem
- **状态**：✓ 已连接
- **命令**：`npx -y @modelcontextprotocol/server-filesystem`

### sequential-thinking
- **状态**：✓ 已连接
- **命令**：`npx -y @modelcontextprotocol/server-sequential-thinking`

### fetch
- **状态**：✓ 已连接
- **命令**：`npx -y @kazuph/mcp-fetch`

### chrome-devtools
- **状态**：✓ 已连接
- **命令**：`npx -y chrome-devtools-mcp@latest`

### github
- **状态**：✓ 已连接
- **命令**：`npx -y @modelcontextprotocol/server-github`

### excel
- **状态**：✓ 已连接
- **命令**：`npx -y @negokaz/excel-mcp-server`

### cclsp
- **状态**：✓ 已连接
- **命令**：`npx -y cclsp@latest`

### memory
- **状态**：✓ 已连接
- **命令**：`npx -y @modelcontextprotocol/server-memory`

### mcp-all-in-one
- **状态**：✓ 已连接
- **命令**：`npx -y mcp-all-in-one@latest stdio`

### playwright
- **状态**：✓ 已连接
- **命令**：`npx @playwright/mcp@latest`

### notebooklm
- **状态**：✓ 已连接
- **命令**：`npx notebooklm-mcp@latest`

### context7
- **状态**：✓ 已连接
- **命令**：`npx @upstash/context7-mcp@latest`

### mcp-echarts
- **状态**：✓ 已连接
- **命令**：`npx -y mcp-echarts`

---

## 三、连接失败 (5个)

### amap
- **状态**：✗ 连接失败
- **命令**：`npx -y @sugarforever/amap-mcp-server`

### brave-search
- **状态**：✗ 连接失败
- **命令**：`npx -y @brave/brave-search-mcp-server -- --brave-api-key`

### e2b
- **状态**：✗ 连接失败
- **命令**：`npx -y @e2b-dev/mcp-server`

### aliyun-asr
- **状态**：✗ 连接失败
- **命令**：`https://dashscope.aliyuncs.com/api/v1/mcps/SpeechToText/sse (SSE)`

### aliyun-tts
- **状态**：✗ 连接失败
- **命令**：`https://dashscope.aliyuncs.com/api/v1/mcps/QwenTextToSpeech/sse (SSE)`

