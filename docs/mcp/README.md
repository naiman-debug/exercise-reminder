# MCP 服务器管理

## 概述

本目录包含自定义 MCP 服务器的配置和管理文档。

## 已配置的 MCP 服务器

### 1. GLM-4.6V-Flash (智谱 AI) ✅ 已测试可用

**用途**: 网页截图和图像分析、文本对话

**配置文件**: `.mcp.json`

**服务器位置**: `temp/inbox/mcp-glm-4.6v-flash/`

**启动脚本**: `start-server.bat`

**环境变量**:
- `GLM_API_KEY`: 智谱 AI API Key

**可用工具**:
- `mcp__glm-flash__analyze_image` - 图像分析（支持 URL）
- `mcp__glm-flash__chat` - 文本对话

**状态**: ✅ 已加载并测试通过

**测试结果** (2026-01-29):
- ✅ 文本对话: 正常工作 (91 tokens/次)
- ✅ 图像分析: 正常工作 (~782 tokens/次)
- ✅ API 响应: 快速稳定

### 2. Vision MCP (SiliconFlow)

**用途**: 通用视觉分析（支持多种模型）

**配置文件**: `.mcp.json`

**可用工具**:
- `mcp__vision-mcp__analyze_image` - 图像分析（支持本地文件）

**状态**: ✅ 已加载并可用

### 3. SearXNG 搜索

**用途**: 网页搜索

**配置文件**: `.mcp.json`

**依赖**: 本地 SearXNG 实例 (http://localhost:8888)

**状态**: ⚠️ 需要本地 SearXNG 服务

## 故障排除

### GLM-Flash MCP 无法启动

**症状**: Claude Code 中无法使用 `mcp__glm-flash__*` 工具

**解决方案**:

1. **检查 API Key**:
   ```bash
   # 验证 API Key 格式
   # 应该是: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxx
   ```

2. **手动测试服务器**:
   ```bash
   cd F:\claude-code\temp\inbox\mcp-glm-4.6v-flash
   set GLM_API_KEY=your_api_key_here
   node index.js
   ```

   应该看到: `GLM-4.6V-Flash MCP server running on stdio`

3. **检查 .mcp.json 配置**:
   ```json
   {
     "mcpServers": {
       "glm-flash": {
         "type": "stdio",
         "command": "F:\\claude-code\\temp\\inbox\\mcp-glm-4.6v-flash\\start-server.bat",
         "args": []
       }
     }
   }
   ```

4. **重启 Claude Code**:
   - 修改配置后需要完全重启 Claude Code

### Vision MCP 无法使用

**检查配置**:
```json
{
  "mcpServers": {
    "vision-mcp": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@lutery/vision-mcp"],
      "env": {
        "VISION_MODEL_TYPE": "siliconflow",
        "VISION_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 添加新的 MCP 服务器

### 步骤

1. **创建服务器目录**:
   ```bash
   mkdir -p temp/inbox/my-mcp-server
   cd temp/inbox/my-mcp-server
   npm init -y
   npm install @modelcontextprotocol/sdk
   ```

2. **创建服务器代码** (`index.js`):
   ```javascript
   #!/usr/bin/env node
   import { Server } from '@modelcontextprotocol/sdk/server/index.js';
   import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

   const server = new Server({
     name: 'my-mcp-server',
     version: '1.0.0',
   }, {
     capabilities: { tools: {} },
   });

   // 实现工具...

   const transport = new StdioServerTransport();
   await server.connect(transport);
   ```

3. **更新 .mcp.json**:
   ```json
   {
     "mcpServers": {
       "my-server": {
         "type": "stdio",
         "command": "node",
         "args": ["F:/claude-code/temp/inbox/my-mcp-server/index.js"],
         "env": {
           "API_KEY": "your_key"
         }
       }
     }
   }
   ```

4. **重启 Claude Code**

## 有用的 MCP 服务器

### 官方服务器
- **GitHub**: 文件操作、仓库管理
- **Filesystem**: 文件系统访问
- **Playwright**: 浏览器自动化
- **Puppeteer**: 浏览器自动化（备用）

### 社区服务器
- **mcp-searxng**: SearXNG 搜索集成
- **@lutery/vision-mcp**: 多模型视觉分析
- **mcp-puppeteer**: Puppeteer 集成

## 相关文档

- [MCP 工具验证指南](MCP_TOOL_VERIFICATION.md) - **工具测试结果**
- [网页截图分析指南](WEB_SCREENSHOT_ANALYSIS_GUIDE.md) - 完整使用指南
- [本地开发截图工作流](LOCAL_DEV_SCREENSHOT_WORKFLOW.md) - 本地开发解决方案
- [MCP 官方文档](https://modelcontextprotocol.io/)

## 快速参考

### 查看已加载的 MCP 工具

在 Claude Code 中执行：
```
列出所有可用的 MCP 工具
```

或使用工具搜索：
```
查找 "mcp" 相关工具
```

### 测试 MCP 工具

```javascript
// 测试 GLM-Flash
mcp__glm-flash__chat({
  prompt: "你好，请介绍一下你自己"
})

// 测试 Vision MCP
mcp__vision-mcp__analyze_image({
  image: "path/to/image.png",
  prompt: "描述这个图片"
})
```

## 贡献

如果你创建了有用的 MCP 服务器，请在这里添加文档。
