# MCP 操作指南

> **更新日期**：2026-01-19
> **用途**：需要复杂操作配置的 MCP 服务器使用指南

---

本文档提供需要额外配置或复杂操作的 MCP 服务器的详细使用说明。

---

## 目录

1. [NotebookLM - AI 知识库](#notebooklm-ai-知识库)
2. [Playwright - 浏览器自动化](#playwright-浏览器自动化)

---

## NotebookLM - AI 知识库

### 什么是 NotebookLM？

**NotebookLM** 是 Google 推出的 AI 知识库工具，由 Gemini 2.5 驱动。你可以上传文档，NotebookLM 会基于这些文档提供**零幻觉**的智能问答。

**核心优势：**
- 🎯 **零幻觉** - 只基于你上传的文档回答，不知道就说不知道
- 🔄 **自动追问** - Claude 会自主深入研究，多轮对话获取完整信息
- 📚 **多文档关联** - 可处理 50+ 文档，自动关联信息
- 🔗 **引用溯源** - 每个答案都包含来源引用

---

### 快速开始

#### 步骤 1：安装 MCP

```bash
claude mcp add --scope user notebooklm npx notebooklm-mcp@latest
```

#### 步骤 2：认证（一次性）

在 Claude Code 中说：

```
"Log me in to NotebookLM"
```

或者

```
"打开 NotebookLM 认证设置"
```

**Chrome 窗口会自动打开**，使用你的 Google 账号登录。

> 💡 **建议**：使用专用的 Google 账号，避免使用主要账号

#### 步骤 3：创建知识库

1. 访问 [notebooklm.google.com](https://notebooklm.google.com)
2. 点击 **Create notebook** 创建笔记本
3. 上传文档：
   - 📄 PDF、Google Docs、Markdown 文件
   - 🔗 网站、GitHub 仓库
   - 🎥 YouTube 视频
   - 📚 可添加多个来源

#### 步骤 4：分享笔记本

1. 点击笔记本右上角的 **⚙️ Share**
2. 选择 **Anyone with link**
3. **复制链接**

#### 步骤 5：在 Claude 中使用

告诉 Claude 使用你的 NotebookLM：

```
"我正在使用 [库名/框架]。这是我的 NotebookLM：[链接]"
```

**就这么简单！** Claude 会自动与 NotebookLM 对话，获取准确信息后再写代码。

---

### 常用命令

| 意图 | 对 Claude 说 | 结果 |
|:-----|:------------|:-----|
| **认证** | "Log me in to NotebookLM" | Chrome 打开登录窗口 |
| **添加笔记本** | "添加 [链接] 到库" | 保存笔记本及元数据 |
| **查看笔记本** | "显示我们的笔记本" | 列出所有保存的笔记本 |
| **选择笔记本** | "使用 React 笔记本" | 设置活动笔记本 |
| **研究优先** | "先用 NotebookLM 研究一下" | 多问题深入研究会话 |
| **查看浏览器** | "显示浏览器" | 实时观看 NotebookLM 对话 |
| **修复认证** | "修复 NotebookLM 认证" | 清除并重新认证 |
| **清理数据** | "运行 NotebookLM 清理" | 删除所有数据重新开始 |

---

### 实战示例

#### 示例 1：构建 n8n 工作流

**问题**：n8n API 很新，Claude 经常幻觉节点名称和功能。

**解决方案**：

```
"帮我构建一个 Gmail 垃圾邮件过滤工作流。使用这个 NotebookLM：[链接]"
```

**AI 对话过程**：

```
Claude → "n8n 中的 Gmail 集成如何工作？"
NotebookLM → "使用 Gmail Trigger 轮询，或 Gmail 节点的 Get Many..."

Claude → "如何解码 base64 邮件正文？"
NotebookLM → "正文在 payload.parts 中 base64url 编码，使用 Function 节点..."

Claude → "如何将 OpenAI 响应解析为 JSON？"
NotebookLM → "设置 responseFormat 为 json，在 IF 节点中使用 {{ $json.spam }}..."

Claude → "如果 API 失败如何处理错误？"
NotebookLM → "使用 Error Trigger 节点，启用 Continue On Fail..."

Claude → ✅ "这是你的完整工作流 JSON..."
```

**结果**：一次成功，无需调试幻觉的 API。

#### 示例 2：学习新框架

```
"我想学习 Next.js 15 的新特性。用这个 NotebookLM 帮我研究：[官方文档链接]"
```

Claude 会：
1. 先问 NotebookLM Next.js 15 有哪些新特性
2. 逐个深入询问每个特性的实现细节
3. 询问最佳实践和注意事项
4. 最后生成完整的学习计划和示例代码

---

### 高级用法

#### 带标签的笔记本管理

```
"添加 [链接] 到库，标记为 '前端, React, 组件'"
```

Claude 会自动根据当前任务选择合适的笔记本。

#### 多账号切换

```
"用不同的 Google 账号重新认证"
```

适合需要隔离不同项目或达到速率限制时。

#### 保留库的清理

```
"清理但保留我的笔记本库"
```

清除所有临时数据，保留你保存的笔记本链接。

---

### 常见问题

**Q: 真的是零幻觉吗？**
A: 是的。NotebookLM 专门设计为只基于上传的来源回答。如果不知道，会直接说不知道。

**Q: 速率限制？**
A: 免费版有每日查询限制。可以快速切换账号继续研究。

**Q: 安全性？**
A: Chrome 在本地运行，凭据不会离开你的机器。建议使用专用 Google 账号。

**Q: 可以看到过程吗？**
A: 可以！说"显示浏览器"即可实时观看 NotebookLM 对话。

**Q: 比本地 RAG 好在哪里？**
A: 无需设置向量数据库、嵌入、分块策略。上传文档即可使用。由 Google Gemini 2.5 处理，质量更高。

---

### 工作流对比

| 方式 | Token 消耗 | 设置时间 | 幻觉率 | 答案质量 |
|:-----|:-----------|:---------|:------|:---------|
| **直接喂文档给 Claude** | 🔴 很高 | 立即 | 高 - 会填补空缺 | 不稳定 |
| **网络搜索** | 🟡 中等 | 立即 | 高 - 来源不可靠 | 碰运气 |
| **本地 RAG** | 🟡 中高 | 数小时 | 中 - 检索缺口 | 取决于配置 |
| **NotebookLM MCP** | 🟢 最少 | 5 分钟 | **零** - 拒绝未知 | 专家级综合 |

---

### 相关链接

- **GitHub**: https://github.com/PleasePrompto/notebooklm-mcp
- **NotebookLM**: https://notebooklm.google.com
- **NPM**: https://www.npmjs.com/package/notebooklm-mcp

---

## Playwright - 浏览器自动化

### 什么是 Playwright？

**Playwright** 是 Microsoft 开发的浏览器自动化框架，支持 Chromium、Firefox 和 WebKit。Playwright MCP 让 Claude 可以直接控制浏览器进行自动化操作。

**核心功能：**
- 🌐 浏览器导航（访问 URL、前进后退、标签页管理）
- 🖱️ 页面交互（点击、输入、悬停、拖拽）
- 📸 快照截图（可访问性快照、页面截图、PDF 导出）
- 🔍 页面分析（网络请求、控制台日志、元素定位）
- 🎯 自动化测试（表单填充、元素验证）

---

### 快速开始

#### 步骤 1：安装 MCP

```bash
claude mcp add --scope user playwright npx @playwright/mcp@latest
```

#### 步骤 2：安装浏览器

```bash
npx -y playwright install chromium firefox webkit
```

下载的浏览器位置：`C:\Users\Administrator\AppData\Local\ms-playwright\`

#### 步骤 3：重启 Claude Code

使 MCP 服务器生效。

---

### 常用操作

#### 导航到网页

```
"打开 https://example.com"
```

#### 点击元素

```
"点击页面上的登录按钮"
```

#### 输入文本

```
"在搜索框中输入 'Hello World'"
```

#### 截图

```
"截取当前页面的屏幕截图"
```

#### 获取页面快照

```
"获取当前页面的可访问性快照"
```

这比截图更有用，因为 Claude 可以理解页面结构并执行操作。

---

### 实战示例

#### 示例 1：网页自动化

```
"打开 https://github.com，点击搜索框，输入 'playwright'，然后按回车"
```

#### 示例 2：表单填充

```
"打开登录页面，填写用户名和密码，然后点击登录按钮"
```

#### 示例 3：数据抓取

```
"打开这个网页，提取所有文章标题和链接"
```

---

### 浏览器选择

默认使用 Chromium。如需切换：

```
"使用 Firefox 浏览器"
```

或

```
"使用 WebKit 浏览器（Safari）"
```

---

### 相关链接

- **GitHub**: https://github.com/microsoft/playwright-mcp
- **官方文档**: https://playwright.dev

---

**文档维护**：如有新的需要复杂操作的 MCP，将添加到此文档。

---

**Sources**:
- [NotebookLM MCP GitHub](https://github.com/PleasePrompto/notebooklm-mcp)
- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
