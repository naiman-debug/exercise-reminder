# 全局文档中心

> 这些文档适用于所有 Claude Code 项目

---

## 📂 目录结构

```
F:\claude-code\docs/
├── README.md          # 本文件 - 文档索引
├── mcp/               # MCP 服务器文档
│   ├── README.md                      # MCP 服务器管理总览
│   ├── MCP_TOOL_VERIFICATION.md       # **新** - MCP 工具测试结果
│   ├── WEB_SCREENSHOT_ANALYSIS_GUIDE.md    # 网页截图分析指南
│   ├── LOCAL_DEV_SCREENSHOT_WORKFLOW.md    # 本地开发截图工作流
│   ├── MCP_SERVERS.md                # MCP 服务器列表
│   └── MCP_USAGE_GUIDE.md            # MCP 使用指南
└── plugin/            # Plugin 使用指南
    └── PLUGIN使用指南.md      # Plugin/MCP 可视化使用指南
```

---

## 📚 文档列表

### 🎮 游戏开发

| 文档 | 说明 |
|------|------|
| [GAME_DEV_GUIDE.md](GAME_DEV_GUIDE.md) | **新** - 使用 Claude Code + Godot 进行游戏开发完整指南 |

### 🛠️ 开发工具

| 文档 | 说明 |
|------|------|
| [TOOL_SELECTION_GUIDE.md](TOOL_SELECTION_GUIDE.md) | **推荐** - 工具选择指南，快速找到合适的工具 |
| [TOOLS_GUIDE.md](TOOLS_GUIDE.md) | Superpowers & OpenSpec 详细使用指南 |

### MCP 服务器

| 文档 | 说明 |
|------|------|
| [mcp/README.md](mcp/README.md) | **推荐** - MCP 服务器管理总览 |
| [MCP_TOOL_VERIFICATION.md](mcp/MCP_TOOL_VERIFICATION.md) | **新** - GLM-Flash 工具测试结果 ✅ 已验证可用 |
| [WEB_SCREENSHOT_ANALYSIS_GUIDE.md](mcp/WEB_SCREENSHOT_ANALYSIS_GUIDE.md) | 网页截图分析完整指南 |
| [LOCAL_DEV_SCREENSHOT_WORKFLOW.md](mcp/LOCAL_DEV_SCREENSHOT_WORKFLOW.md) | 本地开发截图分析工作流程 |
| [MCP_SERVERS.md](mcp/MCP_SERVERS.md) | 所有可用的 MCP 服务器列表和配置 |
| [MCP_USAGE_GUIDE.md](mcp/MCP_USAGE_GUIDE.md) | MCP 使用方法和技巧 |

### Plugin

| 文档 | 说明 |
|------|------|
| [PLUGIN使用指南.md](plugin/PLUGIN使用指南.md) | **推荐首选** - Plugin 和 MCP 可视化使用指南 |

---

## 🎯 什么是全局文档？

**全局文档**是指：
- 适用于所有 Claude Code 项目
- 与具体项目无关的通用工具/服务文档
- 不依赖于特定项目的功能

**判断标准**：
```
┌─────────────────────────────────────────┐
│  这个文档是否：                          │
│                                         │
│  ✅ 解释 Claude Code 的通用功能？        │
│     → 是全局文档，放这里                 │
│                                         │
│  ✅ 说明 Plugin/MCP 的使用方法？         │
│     → 是全局文档，放这里                 │
│                                         │
│  ❌ 特定于某个项目的功能？               │
│     → 不是全局文档，放项目目录           │
└─────────────────────────────────────────┘
```

---

## 📝 与项目文档的区别

| | 全局文档 | 项目文档 |
|---|----------|----------|
| **位置** | `F:\claude-code\docs\` | `{项目}\docs\` |
| **适用范围** | 所有项目 | 特定项目 |
| **示例** | Plugin指南、MCP文档 | 项目特定指南 |
| **更新频率** | 随 Claude Code 更新 | 随项目需求更新 |

---

## 🔗 相关链接

- [全局规则索引](../.global/README.md)
- [文件组织规范](../.global/rules/FILE_ORGANIZATION_RULES.md)
- [Superpowers & OpenSpec 指南](TOOLS_GUIDE.md)

---

> 💡 **提示**：如果你想了解 Plugin 或 MCP 的使用方法，从 [PLUGIN使用指南.md](plugin/PLUGIN使用指南.md) 开始！
>
> **新用户推荐**：查看 [Superpowers & OpenSpec 指南](TOOLS_GUIDE.md) 了解开发工作流程！
