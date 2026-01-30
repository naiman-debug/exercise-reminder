# 脚本目录

> 用于维护全局文档的自动化脚本

---

## 📂 可用脚本

### 1. update-mcp-docs.js / .bat

**功能**：自动扫描已安装的 MCP 服务器并更新文档

**使用方式**：

**Windows**：
```bash
# 双击运行
F:\claude-code\.global\scripts\update-mcp-docs.bat

# 或命令行
node F:\claude-code\.global\scripts\update-mcp-docs.js
```

**Linux/Mac**：
```bash
node F:/claude-code/.global/scripts/update-mcp-docs.js
```

**更新内容**：
- `F:\claude-code\docs\mcp\MCP_SERVERS.md`

**输出示例**：
```
🔍 扫描 MCP 服务器...
✅ 文档已更新：F:\claude-code\docs\mcp\MCP_SERVERS.md
📊 统计：
   - 已连接：17
   - 需要认证：0
   - 连接失败：5
   - 总计：22
```

---

## 🔄 定期更新建议

```
┌─────────────────────────────────────────┐
│  建议每月运行一次更新脚本               │
│                                         │
│  什么时候需要运行？                     │
│  ✅ 安装了新的 MCP 服务器               │
│  ✅ 卸载了某个 MCP 服务器               │
│  ✅ MCP 服务器状态发生变化              │
│  ✅ 每月定期检查                        │
└─────────────────────────────────────────┘
```

---

## 📝 待开发脚本

- [ ] update-plugin-docs.js - 自动更新 Plugin 文档
- [ ] check-docs-consistency.js - 检查文档一致性
- [ ] generate-toc.js - 自动生成目录

---

## ⚙️ 环境要求

- Node.js (已安装)
- Claude Code CLI (`claude` 命令可用)

---

> 💡 **提示**：可以将此目录加入 PATH，方便全局调用
