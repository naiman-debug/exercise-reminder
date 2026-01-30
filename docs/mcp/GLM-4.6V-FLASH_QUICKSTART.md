# GLM-4.6V-Flash MCP 服务器 - 快速开始指南

## 📋 概述

本文档帮助您快速安装和配置 GLM-4.6V-Flash MCP 服务器，集成智谱AI的多模态视觉能力到 Claude Code。

## 🚀 快速开始

### 第一步：获取 API Key

1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册并登录账号
3. 在控制台获取 API Key

### 第二步：配置 MCP 服务器

编辑 `.mcp.json` 文件，将 `your_actual_api_key_here` 替换为您的真实 API Key：

```json
{
  "mcpServers": {
    "glm-4.6v-flash": {
      "type": "stdio",
      "command": "cmd",
      "args": [
        "/c",
        "node",
        "F:/claude-code/temp/inbox/mcp-glm-4.6v-flash/index.js"
      ],
      "env": {
        "GLM_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

### 第三步：安装依赖

```bash
cd temp/inbox/mcp-glm-4.6v-flash
npm install
```

### 第四步：重启 Claude Code

- **VSCode**: 按 `Ctrl+Shift+P`，输入 "Reload Window" 并回车
- 或完全重启 VSCode

## 💡 使用示例

### 图像分析

在 Claude Code 中，您可以直接要求分析图像：

```
请使用 glm-4.6v-flash 服务器的 analyze_image 工具分析这张图片：
prompt: "描述图片中的主要内容、场景和细节"
imageUrl: "https://example.com/image.jpg"
```

### 文本对话

```
请使用 glm-4.6v-flash 服务器的 chat 工具回答这个问题：
"什么是人工智能？"
```

## 🔍 验证安装

安装完成后，您可以询问 Claude：

```
列出所有可用的 MCP 工具
```

您应该能看到 `glm-4.6v-flash` 服务器提供的工具：
- `analyze_image` - 图像分析
- `chat` - 文本对话

## 📚 详细文档

完整文档请参考：[temp/inbox/mcp-glm-4.6v-flash/README.md](../temp/inbox/mcp-glm-4.6v-flash/README.md)

## ⚠️ 注意事项

1. **API Key 安全**：不要将 API Key 提交到版本控制系统
2. **URL 要求**：图像 URL 必须是公开可访问的
3. **配额限制**：注意智谱AI的 API 调用配额
4. **网络连接**：确保能够访问 `open.bigmodel.cn`

## 🐛 常见问题

### Q: 服务器启动失败？
A: 检查 Node.js 版本（需要 >= 18）和依赖是否正确安装

### Q: API 调用报错 401？
A: 验证 API Key 是否正确且有效

### Q: 图像无法分析？
A: 确认图像 URL 可以公开访问，格式支持 PNG/JPG/JPEG

## 📞 获取帮助

- 智谱AI文档：https://open.bigmodel.cn/dev/api
- MCP 协议：https://modelcontextprotocol.io/

---

**最后更新**：2025-01-29
