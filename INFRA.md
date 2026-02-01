# INFRA - 平台能力总览

> **更新日期**：2026-02-01（新增 BMAD 工作流框架）
> **用途**：Claude Code 全部能力总览与快速索引

---

## 📊 能力层级

```
┌─────────────────────────────────────────────────────────────────┐
│  系统级 (C:\Users\Administrator\.claude\)                        │
│  ├─ 插件 (30+ 官方)                                              │
│  ├─ MCP 服务器 (17 个已连接)                                     │
│  ├─ Skills (16 个)                                               │
│  └─ Hooks 配置                                                   │
└─────────────────────────────────────────────────────────────────┘
                          ↓ 继承
┌─────────────────────────────────────────────────────────────────┐
│  平台级 (F:\claude-code\)                                         │
│  ├─ MCP (2 个)                                                   │
│  ├─ Skills (6 个)                                                │
│  ├─ Agents (3 个)                                                │
│  ├─ Tools (Superpowers + OpenSpec)                               │
│  └─ 全局文档 (docs/)                                             │
└─────────────────────────────────────────────────────────────────┘
                          ↓ 继承
┌─────────────────────────────────────────────────────────────────┐
│  项目级 (F:\claude-code\项目X\)                                   │
│  ├─ 项目 MCP/Skills 配置                                          │
│  ├─ Hookify 规则                                                 │
│  └─ 项目使用经验文档                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 目录索引

| 类别 | 文档 | 说明 |
|------|------|------|
| **总览** | 本文件 | 能力总览与索引 |
| **MCP** | [docs/mcp/README.md](docs/mcp/README.md) | MCP 服务器管理 |
| **MCP列表** | [docs/mcp/MCP_SERVERS.md](docs/mcp/MCP_SERVERS.md) | 所有 MCP 服务器 |
| **MCP使用** | [docs/mcp/MCP_USAGE_GUIDE.md](docs/mcp/MCP_USAGE_GUIDE.md) | MCP 操作指南 |
| **Plugin** | [docs/plugin/PLUGIN使用指南.md](docs/plugin/PLUGIN使用指南.md) | Plugin 使用指南 |
| **工具** | [docs/TOOLS_GUIDE.md](docs/TOOLS_GUIDE.md) | Superpowers & OpenSpec |
| **工具选择** | [docs/TOOL_SELECTION_GUIDE.md](docs/TOOL_SELECTION_GUIDE.md) | 工具快速选择 |
| **归档** | [temp/infra-archive-2026-01-28/](temp/infra-archive-2026-01-28/) | 旧版技能/MCP文档 |

---

## 1️⃣ 系统级 MCP 服务器

**位置**：`C:\Users\Administrator\.claude.json`
**状态**：17 个已连接

### ✅ 已连接 (17个)

| MCP | 功能 | 优先级 | 评分 |
|-----|------|--------|------|
| **chrome-devtools** | Chrome 开发工具 | 🟡 中 | - |
| **context7** | 技术文档查询 | 🔴 高 | - |
| **excel** | Excel 操作 | 🟢 低 | - |
| **fetch** | HTTP 请求 | 🟡 中 | - |
| **filesystem** | 文件系统操作 | 🔴 高 | - |
| **github** | GitHub 操作 | 🟡 中 | - |
| **mcp-all-in-one** | MCP 聚合器 | 🟢 低 | - |
| **mcp-echarts** | 图表生成 | 🟢 低 | - |
| **memory** | 记忆存储 | 🟡 中 | - |
| **notebooklm** | AI 知识库（零幻觉） | 🔴 高 | - |
| **playwright** | 浏览器自动化 | 🟡 中 | - |
| **pencil** | Pencil Dev 集成 | 🟢 低 | - |
| **sequential-thinking** | 序列思考 | 🟢 低 | - |
| **web-reader** | 网页内容读取 | 🔴 高 | - |
| **web-search-prime** | 网络搜索 | 🔴 高 | - |
| **zai-mcp-server** | UI/UX 分析、设计验证 | 🔴 高 | ⭐⭐⭐⭐⭐ |
| **zread** | 文档搜索读取 | 🟡 中 | - |

### 🔍 重点 MCP 详解

#### zai-mcp-server ⭐⭐⭐⭐⭐
**功能**：专业 UI/UX 图像理解与分析

**测试评分**：95/100
- ✅ UI 分析准确性：精确提取颜色代码、字号、间距、圆角
- ✅ 专业术语：使用标准 UI/UX 术语（WCAG 2.1、卡片式布局）
- ✅ 分析深度：7 个维度完整分析
- ✅ 可操作性：提供具体改进建议

**适用场景**：
- ✅ UI/UX 设计验证
- ✅ 原型设计评审
- ✅ 可访问性审计
- ✅ 设计规范符合度检查

**参数**：`image`, `prompt`, `output_format?`, `template?`
**模板**：ui-analysis, ocr, object-detection

---

### 🔧 MCP 详细文档

- [MCP 服务器总览](docs/mcp/MCP_SERVERS.md) - 完整列表和配置
- [MCP 使用指南](docs/mcp/MCP_USAGE_GUIDE.md) - NotebookLM、Playwright 等详细教程

---

## 2️⃣ 系统级 Skills

**位置**：`C:\Users\Administrator\.claude\skills\`
**来源**：官方插件 + everything-claude-code
**总数**：16 个

### 🔴 核心 Skills

| Skill | 功能 | 触发条件 |
|-------|------|----------|
| **brainstorming** | 头脑风暴，细化需求 | 创造性工作前 |
| **writing-plans** | 编写实现计划 | 设计确认后 |
| **executing-plans** | 执行计划 | 计划确认后 |
| **backend-patterns** | 后端架构模式 | Node.js/Express 后端 |
| **frontend-design** | 前端界面设计 | 创建 UI 组件 |
| **security-review** | 安全审查 | 敏感数据处理 |

### 🟡 常用 Skills

| Skill | 功能 |
|-------|------|
| **test-driven-development** | TDD 测试驱动 |
| **systematic-debugging** | 系统化调试 |
| **verification-before-completion** | 完成前验证 |
| **continuous-learning** | 持续学习，提取模式 |
| **design-check** | 设计检查 |

### 🟢 开发 Workflow Skills

| Skill | 功能 |
|-------|------|
| **subagent-driven-development** | 子代理驱动开发 |
| **finishing-a-development-branch** | 完成分支开发 |
| **verification-loop** | 验证循环 |

### 🔵 代码审查 Skills

| Skill | 功能 |
|-------|------|
| **requesting-code-review** | 请求代码审查 |
| **receiving-code-review** | 接收代码审查 |

### 📚 文件规划 Skills

| Skill | 功能 |
|-------|------|
| **planning-with-files** | 基于文件的规划 |
| **using-superpowers** | Superpowers 使用指南 |

### 📚 归档文档

- [SKILL-00: 总览](temp/infra-archive-2026-01-28/SKILL-00-总览.md)
- [SKILL-01: 内置](temp/infra-archive-2026-01-28/SKILL-01-内置.md)
- [SKILL-02: 全局](temp/infra-archive-2026-01-28/SKILL-02-全局.md)

---

## 3️⃣ 系统级插件

**位置**：`C:\Users\Administrator\.claude\plugins\`
**总数**：30+ 官方插件（2026-01-31 更新）

### 🎨 设计开发

| 插件 | 功能 |
|------|------|
| **frontend-design** | 前端界面设计 |
| **feature-dev** | 快速功能开发 |
| **code-review** | 代码审查 |
| **plugin-dev** | 插件开发 |
| **figma** | Figma 设计集成（代码生成） |
| **superpowers** | 完整开发工作流框架 |

### 🔧 开发工具

| 插件 | 功能 |
|------|------|
| **playwright** | 浏览器自动化测试 |
| **commit-commands** | Git 提交命令 |
| **pr-review-toolkit** | PR 审查工具 |
| **code-simplifier** | 代码简化 |
| **pyright-lsp** | Python 语言服务器 |
| **typescript-lsp** | TypeScript 语言服务器 |

### 📚 文档查询

| 插件 | 功能 |
|------|------|
| **context7** | 技术文档查询 |

### 🌐 集成服务

| 插件 | 功能 |
|------|------|
| **github** | GitHub 集成 |
| **supabase** | Supabase 集成 |
| **atlassian** | Jira/Confluence/Compass 集成 |
| **sentry** | Sentry 错误监控集成 |

### 🤖 AI 助手

| 插件 | 功能 |
|------|------|
| **serena** | Serena AI 助手 |
| **ralph-loop** | Ralph 重构循环 |
| **ralph-wiggum** | 代码转换 |

### 🔒 安全质量

| 插件 | 功能 |
|------|------|
| **security-guidance** | 安全指导 |
| **agent-sdk-dev** | Agent SDK 开发 |

### 📝 其他

| 插件 | 功能 |
|------|------|
| **hookify** | Hook 管理 |
| **glm-plan-bug** | GLM Bug 反馈 |
| **glm-plan-usage** | GLM 使用查询 |
| **claude-opus-4-5-migration** | 模型迁移 |
| **explanatory-output-style** | 说明性输出 |
| **learning-output-style** | 学习风格输出 |
| **claude-code-setup** | 自动化设置推荐 |
| **claude-md-management** | CLAUDE.md 文件管理 |

---

## 4️⃣ Hook / Hookify

**位置**：`C:\Users\Administrator\.claude\settings.json`
**命令**：`/hookify:hookify`, `/hookify:list`, `/hookify:configure`

### 功能

创建自动化规则，控制对话行为：
- 防止敏感话题
- 设置代码规范
- 限制操作范围
- 自动化检查

### 使用文档

- [PLUGIN使用指南.md](docs/plugin/PLUGIN使用指南.md) - Hookify 使用说明

---

## 5️⃣ 平台级能力

**位置**：`F:\claude-code\.claude\` + `tools/`

### MCP (2个)

| 名称 | 功能 | 文档 |
|------|------|------|
| **searxng** | 本地元搜索 | [MCP-01](temp/infra-archive-2026-01-28/MCP-01-searxng.md) |
| **vision-mcp** | AI 图像生成（Silicon Flow） | [MCP-02](temp/infra-archive-2026-01-28/MCP-02-vision-mcp.md) |

### Skills (6个)

| 名称 | 功能 |
|------|------|
| **backend-patterns** | 后端架构模式 |
| **planning-with-files** | 基于文件的规划 |
| **requesting-code-review** | 请求代码审查 |
| **security-review** | 安全审查 |
| **test-driven-development** | TDD 测试驱动 |
| **learned/** | 学习存储目录 |

### Agents (3个)

| 名称 | 功能 |
|------|------|
| **architect** | 架构设计 |
| **build-error-resolver** | 构建错误修复 |
| **security-reviewer** | 安全审查 |

### Tools (3个)

| 工具 | 功能 | 文档 |
|------|------|------|
| **BMAD** | 全栈工作流框架 (软件/游戏/测试) | [_bmad/](.claude/commands/) |
| **Superpowers** | 完整开发工作流 | [tools/superpowers/](tools/superpowers/) |
| **OpenSpec** | 规范管理 | [tools/OpenSpec-Chinese/](tools/OpenSpec-Chinese/) |

---

## 6️⃣ 项目级能力（示例：exercise-reminder-v3）

**位置**：`F:\claude-code\exercise-reminder-v3\.claude\`

### 项目结构

```
exercise-reminder-v3/
├── .claude/
│   ├── settings.json                                    # 项目配置
│   ├── hookify.design-verify-reminder.local.md         # Hookify 规则
│   └── scripts/
│       └── design-verify.js                            # 设计验证脚本
├── .playwright-mcp/                                     # 截图缓存
└── docs/
    ├── SKILLS-MCP-GUIDE.md                            # 工具使用经验
    ├── MCP-TEST-REPORT.md                             # MCP 测试报告
    └── zai-vs-glm-comparison-v2.md                     # MCP 对比分析
```

### 项目级配置内容

| 文件 | 功能 |
|------|------|
| `hookify.design-verify-reminder.local.md` | 原型修改后自动提醒设计验证 |
| `scripts/design-verify.js` | 设计验证脚本 |
| `docs/SKILLS-MCP-GUIDE.md` | 项目 Skills/MCP 使用经验总结 |
| `docs/MCP-TEST-REPORT.md` | Vision MCP 测试报告 |
| `docs/zai-vs-glm-comparison-v2.md` | zai vs GLM 对比分析 |

### 项目使用经验总结

**推荐 MCP 工具**：
- **zai-mcp-server** ⭐⭐⭐⭐⭐ - 专业 UI/UX 分析（评分 95/100）
- **glm-flash** ⭐⭐⭐⭐ - 快速响应、中文友好
- **cclsp** - 代码导航和诊断
- **filesystem** - 文件操作

**推荐 Skills**：
- **test-driven-development** - TDD 测试驱动
- **security-review** - 安全审查
- **backend-patterns** - 后端架构模式
- **brainstorming** - 需求细化

---

## 7️⃣ everything-claude-code 插件

**来源**：第三方插件
**位置**：`C:\Users\Administrator\.claude\plugins\everything-claude-code\`

### 提供内容

| 类型 | 数量 | 说明 |
|------|------|------|
| **Agents** | 11+ | architect, build-error-resolver, code-reviewer 等 |
| **Skills** | 9+ | backend-patterns, frontend-patterns, continuous-learning 等 |
| **Commands** | 15 | /tdd, /plan, /e2e, /build-fix 等 |
| **Rules** | 8 | security, coding-style, testing, git-workflow 等 |
| **Hooks** | 6 | PreToolUse, PostToolUse, SessionStart 等 |

---

## 8️⃣ 新增插件详解（2026-01-31）

### superpowers ⭐⭐⭐⭐⭐
**版本**：4.1.1 | **来源**：官方

**功能**：完整的软件开发工作流程框架

**提供内容**：
- Agents: architect, build-error-resolver, security-reviewer
- Skills: brainstorming, writing-plans, executing-plans, test-driven-development
- Commands: /plan, /tdd, /build-fix, /e2e 等
- Hooks: PreToolUse, PostToolUse, SessionStart 等

**使用场景**：
- 完整的项目开发工作流
- 团队协作标准化
- 自动化测试和质量保证

---

### figma ⭐⭐⭐⭐⭐
**版本**：1.0.0 | **来源**：官方

**功能**：Figma 设计到代码集成

**核心能力**：
- 从 Figma 设计生成代码（React + Tailwind 默认）
- 提取设计上下文（变量、组件、布局）
- Code Connect 集成（复用实际组件）
- 支持桌面和远程 MCP 服务器

**工具**：
- `get_design_context` - 获取设计上下文
- `get_variable_defs` - 获取变量定义
- `get_code_connect_map` - 获取代码组件映射
- `get_screenshot` - 获取截图
- `create_design_system_rules` - 创建设计系统规则

**使用场景**：
- 产品团队构建新流程
- 从 Figma 设计直接生成代码
- 设计系统和组件工作流

---

### atlassian ⭐⭐⭐⭐
**版本**：7caef65e1070 | **来源**：官方

**功能**：Jira、Confluence、Compass 集成

**核心能力**：
- 搜索和总结 Jira/Confluence 内容
- 创建和更新 issues 和页面
- 自动化重复工作（从会议笔记生成 tickets）
- OAuth 2.1 安全授权

**支持产品**：
- Jira - 问题跟踪
- Confluence - 文档协作
- Compass - 服务组件管理

**使用场景**：
- 从会议笔记自动生成 Jira tickets
- 查询和总结 Confluence 文档
- 管理 Compass 服务依赖关系

---

### pyright-lsp ⭐⭐⭐
**版本**：1.0.0 | **来源**：官方

**功能**：Python 语言服务器（Pyright）

**支持扩展**：`.py`, `.pyi`

**安装方式**：
```bash
npm install -g pyright
# 或
pip install pyright
# 或
pipx install pyright
```

**使用场景**：
- Python 静态类型检查
- 代码智能提示
- LSP 功能集成

---

### claude-code-setup ⭐⭐⭐⭐
**版本**：1.0.0 | **来源**：官方

**功能**：自动化 Claude Code 设置推荐

**核心能力**：
- 分析代码库并推荐自动化方案
- 推荐 MCP 服务器
- 推荐 Skills
- 推荐 Hooks 规则
- 推荐 Subagents
- 推荐斜杠命令

**特点**：
- 只读模式，不修改文件
- 针对项目定制化推荐
- 覆盖完整的自动化类别

**使用方法**：
```
"recommend automations for this project"
"help me set up Claude Code"
"what hooks should I use?"
```

---

### sentry ⭐⭐⭐⭐
**版本**：1.0.0 | **来源**：官方

**功能**：Sentry 错误监控和性能分析集成

**核心能力**：

**斜杠命令**：
- `/seer <自然语言查询>` - 自然语言查询 Sentry 环境
- `/getIssues [projectName]` - 获取最近的 issues

**子代理**：
- `issue-summarizer` - 并行分析多个 Sentry issues

**Skills**：
- `sentry-code-review` - 自动分析和修复 PR 中的 Sentry bugs

**使用场景**：
- 自然语言查询错误和性能问题
- 分析和总结多个 issues
- 自动修复 PR 中检测到的问题

---

### claude-md-management ⭐⭐⭐⭐
**版本**：1.0.0 | **来源**：官方

**功能**：CLAUDE.md 文件管理和维护

**两个互补工具**：

**Skill: claude-md-improver**
- 审核 CLAUDE.md 文件质量
- 与代码库状态对比
- 推荐更新建议

**Command: /revise-claude-md**
- 捕获会话学习内容
- 更新项目记忆

**使用场景**：
- 定期维护 CLAUDE.md 文件
- 会话后发现缺少上下文时更新

---

### explanatory-output-style ⭐⭐⭐
**版本**：27d2b86d72da | **来源**：官方

**功能**：说明性输出风格

**用途**：调整 AI 输出风格，提供更详细的解释和说明

---

## 9️⃣ BMAD 工作流框架

**位置**：`F:\claude-code\_bmad\`
**版本**：最新 | **安装方式**：`npx bmad-method install`
**命令**：`/bmad-help` 查看所有工作流

### 模块总览

| 模块 | 功能 | 适用场景 |
|------|------|----------|
| **BMM** | 软件开发全流程 | 标准 Web/移动应用开发 |
| **BMB** | BMAD 构建器 | 扩展 BMAD（自定义代理/模块/工作流） |
| **CIS** | 创新套件 | 设计思维、创新策略、问题解决 |
| **GDS** | 游戏开发套件 | Unity/Unreal/Godot 游戏项目 |
| **TEA** | 测试卓越架构 | 测试框架、CI/CD、TDD/ATDD |

### BMM - 软件开发工作流 (核心模块)

**流程阶段**：
1. **1-Analysis** - Brainstorming → Research → Product Brief
2. **2-Planning** - PRD → UX Design
3. **3-Solutioning** - Architecture → Epics & Stories → Implementation Readiness
4. **4-Implementation** - Sprint Planning → Story Development → Code Review → Retrospective

**核心工作流**：
- `/bmad-bmm-create-prd` - 创建产品需求文档
- `/bmad-bmm-create-architecture` - 创建技术架构
- `/bmad-bmm-create-epics-and-stories` - 创建史诗和用户故事
- `/bmad-bmm-sprint-planning` - Sprint 规划
- `/bmad-bmm-dev-story` - 开发用户故事
- `/bmad-bmm-code-review` - 代码审查

**快速流程**：
- `/bmad-bmm-quick-spec` - 快速技术规范
- `/bmad-bmm-quick-dev` - 快速开发

### BMB - BMAD 构建器

用于创建和扩展 BMAD 框架本身：
- `/bmad-bmb-agent` - 创建/编辑/验证 BMAD 代理
- `/bmad-bmb-module` - 创建/编辑/验证 BMAD 模块
- `/bmad-bmb-workflow` - 创建/编辑/验证 BMAD 工作流

### CIS - 创新套件

创意和设计思维工作流：
- `/bmad-cis-brainstorming` - 头脑风暴
- `/bmad-cis-design-thinking` - 设计思维
- `/bmad-cis-innovation-strategy` - 创新策略
- `/bmad-cis-problem-solving` - 系统化问题解决
- `/bmad-cis-storytelling` - 叙事构建

### GDS - 游戏开发套件

完整的游戏开发工作流：
- `/bmad-gds-create-game-brief` - 游戏简报
- `/bmad-gds-create-gdd` - 游戏设计文档
- `/bmad-gds-game-architecture` - 游戏架构
- `/bmad-gds-sprint-planning` - 游戏开发 Sprint
- `/bmad-gds-dev-story` - 游戏功能开发
- `/bmad-gds-gametest-*` - 游戏测试系列

### TEA - 测试卓越架构

测试架构和质量保证：
- `/bmad-tea-testarch-framework` - 初始化测试框架
- `/bmad-tea-testarch-ci` - CI/CD 质量管道
- `/bmad-tea-testarch-atdd` - 验收测试驱动开发
- `/bmad-tea-testarch-automate` - 测试自动化扩展
- `/bmad-tea-testarch-test-review` - 测试质量评审
- `/bmad_tea_teach-me-testing` - 测试教学 (7 会话课程)

### 核心功能

- `/bmad-brainstorming` - 交互式头脑风暴
- `/bmad-party-mode` - 多代理对话
- `/bmad-help` - 显示所有可用工作流

---

## 🎯 快速使用指南

### 搜索网络/查最新文档
→ **web-search-prime** 或 **searxng** MCP

### UI/UX 设计分析 ⭐
→ **zai-mcp-server** MCP（专业、精确）

### Figma 设计到代码 ⭐⭐⭐
→ **figma** 插件（Figma 集成、代码生成）
- `get_design_context` - 获取设计上下文
- `get_variable_defs` - 获取变量定义
- 支持 React + Tailwind 等多种框架

### AI 绘图创作
→ **vision-mcp** MCP（Silicon Flow）

### 完整开发工作流 ⭐⭐⭐
→ **superpowers** 插件（完整工作流框架）
- `/plan` - 编写计划
- `/tdd` - 测试驱动开发
- `/build-fix` - 修复构建错误

### BMAD 全栈工作流 ⭐⭐⭐⭐⭐
→ **BMAD** 框架（软件/游戏/测试）
- `/bmad-bmm-create-prd` - 创建 PRD
- `/bmad-bmm-create-architecture` - 创建技术架构
- `/bmad-bmm-sprint-planning` - Sprint 规划
- `/bmad-bmm-quick-dev` - 快速开发
- `/bmad-help` - 查看所有工作流

### 快速开发功能
→ **feature-dev** 插件

### 设计 UI
→ **frontend-design** 插件

### 审查代码
→ **code-review** 插件

### 项目自动化设置 ⭐
→ **claude-code-setup** 插件
- "recommend automations for this project"
- 分析代码库并推荐 MCP/Skills/Hooks

### CLAUDE.md 管理 ⭐
→ **claude-md-management** 插件
- `/revise-claude-md` - 捕获会话学习
- "audit my CLAUDE.md" - 审核文件质量

### Sentry 错误监控 ⭐
→ **sentry** 插件
- `/seer <查询>` - 自然语言查询
- `/getIssues [项目]` - 获取最近 issues

### Atlassian 集成 ⭐
→ **atlassian** 插件
- Jira/Confluence/Compass 集成
- 自动创建 tickets、查询文档

### 创建新功能
1. `brainstorming` Skill
2. `writing-plans` Skill
3. `executing-plans` Skill

### 修复 Bug
1. `systematic-debugging` Skill
2. `test-driven-development` Skill

### 理解代码库
→ **Explore** Agent (通过 Task 工具)

### 设计架构
→ **Plan** Agent 或 **architect** Agent

### 修复构建错误
→ **build-error-resolver** Agent

### GitHub 操作
→ **github** 插件

### Python 开发
→ **pyright-lsp** 插件（Python 语言服务器）

### 设置自动化规则
→ `/hookify:hookify` 命令

---

## 📂 配置文件位置

| 级别 | 类型 | 位置 |
|------|------|------|
| **系统级** | 插件 | `C:\Users\Administrator\.claude\plugins\` |
| **系统级** | Skills | `C:\Users\Administrator\.claude\skills\` |
| **系统级** | Hooks | `C:\Users\Administrator\.claude\settings.json` |
| **系统级** | MCP | `C:\Users\Administrator\.claude.json` |
| **系统级** | CClSP | `C:\Users\Administrator\.claude\cclsp.json` |
| **平台级** | MCP | `F:\claude-code\.mcp.json` |
| **平台级** | Skills | `F:\claude-code\.claude\skills\` |
| **平台级** | Agents | `F:\claude-code\.claude\agents\` |
| **平台级** | Tools | `F:\claude-code\tools\` |
| **项目级** | 配置 | `{项目}\.claude\` |
| **项目级** | 经验文档 | `{项目}\docs\` |

---

## 📝 维护记录

| 日期 | 动作 | 说明 |
|------|------|------|
| 2026-02-01 | 工具更新 | 新增 BMAD 工作流框架 (bmm/bmb/cis/gds/tea)，提供完整的软件开发、创新、游戏开发和测试工作流 |
| 2026-01-31 | 内容修正 | 移除已删除的 MCP（cclsp、glm-flash），更新系统级 MCP 数量 22→17，系统级 Skills 数量 30→16 |
| 2026-01-31 | 内容修正 | 更新平台级 Skills 数量 16→6，移除不存在的 Skills |
| 2026-01-31 | 插件更新 | 新增 8 个官方插件（superpowers、figma、atlassian、pyright-lsp、claude-code-setup、sentry、claude-md-management、explanatory-output-style） |
| 2026-01-31 | 重大更新 | 补充系统级 MCP、Skills、LSP 完整列表 |
| 2026-01-31 | 更新 | 添加目录索引和关联文档链接 |
| 2026-01-31 | 更新 | 添加项目级能力示例 |
| 2026-01-28 | 创建 | 初始化能力总览 |

---

> **使用说明**：
> - **系统级能力**自动继承，无需配置
> - **平台级能力**通过 `F:\claude-code\` 继承到所有项目
> - **项目级能力**在项目目录内配置
> - 点击表格中的链接跳转到详细文档
> - 使用 `/` 命令快速调用插件（如 `/hookify:list`）
>
> **MCP 视觉分析工具选择建议**：
> - UI/UX 专业分析 → **zai-mcp-server** ⭐⭐⭐⭐⭐
> - AI 绘图创作 → **vision-mcp**（平台级，需配置）
