# MCP 工具验证指南

## ✅ GLM-Flash MCP 工具状态 - 已验证可用

**最后更新**: 2026-01-29
**测试状态**: ✅ 全部通过

根据实际测试，以下工具**已成功加载并正常工作**：

| 工具名称 | 状态 | 功能 | 测试结果 | Token 消耗 |
|---------|------|------|----------|-----------|
| `mcp__glm-flash__analyze_image` | ✅ 已测试 | 图像分析 | ✅ 通过 | ~782 tokens/次 |
| `mcp__glm-flash__chat` | ✅ 已测试 | 文本对话 | ✅ 通过 | ~91 tokens/次 |

### 📊 详细测试结果

#### 测试 1: 文本对话 (2026-01-29)

**测试命令**:
```javascript
mcp__glm-flash__chat({
  prompt: "你好，请用一句话介绍你自己"
})
```

**结果**: ✅ 成功
```
响应: "我是一个多领域知识库机器人，擅长回答各种问题..."
Token 使用: 66 prompt + 25 completion = 91 total
响应速度: 快速
```

#### 测试 2: 图像分析 (2026-01-29)

**测试命令**:
```javascript
mcp__glm-flash__analyze_image({
  imageUrl: "https://picsum.photos/800/600",
  prompt: "请描述这张图片的内容和风格"
})
```

**结果**: ✅ 成功
```
响应: "这张照片展示了一个年轻男子坐在一间旧房子的角落里..."
Token 使用: 677 prompt + 105 completion = 782 total
响应质量: 详细、准确
```

**结论**: GLM-4.6V-Flash MCP 服务器完全正常工作，所有功能均已验证通过。

---

## 🔍 如何验证 MCP 工具是否可用

### 方法 1: 在 Claude Code 对话中直接测试

**测试 1: 文本对话**
```
请使用 GLM-Flash 问我好
```

Claude 应该会调用 `mcp__glm-flash__chat` 工具。

**测试 2: 图像分析**
```
请使用 GLM-Flash 分析这个图片：https://picsum.photos/800/600
```

Claude 应该会调用 `mcp__glm-flash__analyze_image` 工具。

### 方法 2: 使用工具搜索

在 Claude Code 中输入：
```
搜索 glm 相关的 MCP 工具
```

应该会找到：
- `mcp__glm-flash__analyze_image`
- `mcp__glm-flash__chat`

### 方法 3: 检查 MCP 配置

1. 打开 `.mcp.json`
2. 确认有以下配置：
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

---

## 🐛 为什么你可能认为工具不可用

### 可能原因 1: 搜索关键词不对

❌ **错误的搜索**：
```
搜索 "glm-4.6v-flash"
搜索 "46v"
搜索 "zhipu"
```

✅ **正确的搜索**：
```
搜索 "glm"
搜索 "flash"
搜索 "analyze_image"
```

### 可能原因 2: MCP 客户端缓存

如果你修改了配置后没有完全重启 VSCode，可能会看到旧的工具名称。

**解决方案**：
1. 完全关闭 VSCode（不是重新加载窗口）
2. 等待 5 秒
3. 重新打开项目
4. 等待 MCP 服务器加载（通常需要 3-5 秒）

### 可能原因 3: 服务器启动延迟

MCP 服务器启动需要时间，特别是在 Windows 上。

**如何确认服务器已启动**：
1. 打开 VSCode 的"输出"面板
2. 选择"Model Context Protocol"频道
3. 查找类似这样的日志：
   ```
   GLM-4.6V-Flash MCP server running on stdio
   ```

---

## 🎯 实际使用示例

### 示例 1: 分析在线截图

```
请使用 GLM-Flash 分析这个网页截图：
https://raw.githubusercontent.com/username/screenshots/main/example.png

重点关注：
- 页面布局结构
- 主要功能区域
- 用户交互设计
```

### 示例 2: 分析本地开发服务器

由于 GLM API 需要公网可访问的 URL，你需要：

1. **截图并上传到图床**：
   ```bash
   # 使用 Playwright 截图
   # 然后上传到 GitHub、ImgBB 等
   ```

2. **使用 GLM-Flash 分析**：
   ```
   请分析我本地开发服务器的截图：
   https://your-image-host.com/screenshot.png
   ```

### 示例 3: 纯文本对话

```
使用 GLM-Flash 帮我总结这篇文档的主要内容
```

---

## 🔄 替代方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **GLM-Flash MCP** | 速度快、便宜、中文友好 | 需要公网 URL | ⭐⭐⭐⭐ |
| **Vision MCP** | 可能支持本地文件 | 依赖 SiliconFlow | ⭐⭐⭐⭐⭐ |
| **zai-mcp-server** | 功能强大、稳定 | 可能较慢 | ⭐⭐⭐⭐⭐ |
| **4.5V MCP** | Claude 品质保证 | 最贵 | ⭐⭐⭐ |

---

## 🛠️ 故障排除

### 问题: "Unknown tool: glm-flash_analyze_image"

**原因**: 工具名称格式错误

**解决**: 使用正确的工具名称格式
- ✅ `mcp__glm-flash__analyze_image`
- ❌ `glm-flash_analyze_image`
- ❌ `glm_flash_analyze_image`

### 问题: "图片输入格式/解析错误"

**原因**: GLM API 不支持图片 URL 格式

**解决方案**:
1. 使用简单的公共 URL（GitHub Raw、ImgBB）
2. 避免使用带有签名的临时 URL
3. 确保 URL 可以直接访问（不需要认证）

### 问题: MCP 服务器启动失败

**检查清单**:
- [ ] `start-server.bat` 存在且路径正确
- [ ] `GLM_API_KEY` 环境变量已设置
- [ ] `node_modules` 已安装（运行 `npm install`）
- [ ] Node.js 版本 >= 18

---

## 📝 最佳实践

### 1. 图像 URL 管理

**推荐使用 GitHub 作为图床**：
```bash
# 创建截图仓库
git clone https://github.com/YOUR_USERNAME/screenshots.git

# 添加截图
cp screenshot.png screenshots/
cd screenshots
git add .
git commit -m "Add screenshot"
git push

# 获取 URL
# https://raw.githubusercontent.com/YOUR_USERNAME/screenshots/main/screenshot.png
```

### 2. API Key 安全

⚠️ **重要**：不要将 API Key 提交到 Git

```bash
# .gitignore
.env
*.bat
```

### 3. 成本控制

GLM-4V Flash 按调用次数计费：
- 建议批量分析以提高效率
- 使用缓存避免重复分析
- 监控 API 使用量

---

## 🎉 结论

**GLM-Flash MCP 工具已经可用！**

你现在就可以：
1. ✅ 在对话中直接请求图像分析
2. ✅ 使用 GLM-Flash 进行文本对话
3. ✅ 结合其他工具（Playwright 截图 + GLM-Flash 分析）

如果遇到问题，请检查：
- VSCode 是否完全重启
- MCP 服务器是否启动成功
- 工具名称是否正确

需要帮助？查看 [MCP 服务器管理](README.md) 或 [本地开发截图工作流](LOCAL_DEV_SCREENSHOT_WORKFLOW.md)。
