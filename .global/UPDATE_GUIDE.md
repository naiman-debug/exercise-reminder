# MCP & Plugin 文档更新指南

> 当安装新的 MCP 服务器或 Plugin 后，需要更新全局文档

---

## 🔄 问题说明

当前 MCP 和 Plugin 文档是**静态维护**的，不会自动更新。当安装新服务后，需要手动更新文档。

---

## 📋 更新流程

### 方式一：自动更新（推荐）

```bash
# 运行更新脚本
node F:/claude-code/.global/scripts/update-mcp-docs.js
```

### 方式二：手动更新

#### 步骤 1：获取当前 MCP 列表

```bash
claude mcp list > mcp-list.txt
```

#### 步骤 2：更新文档

根据输出更新：
- `F:\claude-code\docs\mcp\MCP_SERVERS.md`
- `F:\claude-code\docs\plugin\PLUGIN使用指南.md`

#### 步骤 3：更新日期

在文档顶部更新更新日期：
```markdown
> **更新日期**：YYYY-MM-DD
```

---

## 📝 当前 MCP 服务器列表

### ✅ 已连接 (19个)
- context7
- web-search-prime
- zai-mcp-server
- web-reader
- zread
- filesystem
- sequential-thinking
- fetch
- chrome-devtools
- github (npx版本)
- excel
- cclsp
- memory
- mcp-all-in-one
- playwright
- notebooklm
- mcp-echarts

### ⚠️ 需要认证 (1个)
- supabase

### ✗ 连接失败 (若干)
- github (plugin版本)
- serena
- amap
- brave-search
- e2b
- aliyun-asr
- aliyun-tts

---

## 🧩 Plugin 列表

当前已安装的 Plugin：
- code-review
- feature-dev
- frontend-design
- agent-sdk-dev
- hookify (包含5个子命令)
- glm-plan-usage:usage-query
- glm-plan-bug:case-feedback

---

## ⚠️ 注意事项

1. **定期更新**：建议每月检查一次 MCP 和 Plugin 列表
2. **版本控制**：文档更新后提交 git 记录
3. **测试验证**：更新后验证文档与实际安装一致

---

## 📌 待实现功能

- [ ] 自动检测新安装的 MCP/Plugin
- [ ] 自动更新文档脚本
- [ ] 定时任务自动检查更新

---

> 💡 **提示**：如果你安装了新的 MCP 或 Plugin，请记得更新此文档！
