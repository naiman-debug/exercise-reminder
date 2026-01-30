# INFRA - 平台能力总览

> F:\claude-code\ 可用能力总览（系统级 + 平台级）

---

## 📊 全部能力一览

### 系统级插件 (C:\Users\Administrator\.claude\plugins\)
> 默认可用，自动继承

| 插件 | 功能 | 何时使用 |
|------|------|----------|
| **agent-sdk-dev** | Agent SDK 开发 | 开发自定义 Agent |
| **claude-opus-4-5-migration** | 模型迁移 | Opus 4→5 迁移 |
| **code-review** | 代码审查 | 审查代码质量 |
| **code-simplifier** | 代码简化 | 简化复杂代码 |
| **commit-commands** | Git 提交命令 | Git 操作 |
| **context7** | 文档查询 | 查询库文档 |
| **explanatory-output-style** | 说明性输出 | 详细解释 |
| **feature-dev** | 快速功能开发 | 快速实现功能 |
| **frontend-design** | 前端设计 | 设计 UI 界面 |
| **github** | GitHub 集成 | PR/Issue 管理 |
| **glm-plan-bug** | GLM Bug 反馈 | 提交案例反馈 |
| **glm-plan-usage** | GLM 使用查询 | 查询使用统计 |
| **hookify** | Hook 管理 | 配置自动化规则 |
| **learning-output-style** | 学习风格输出 | 提取可复用模式 |
| **plugin-dev** | 插件开发 | 开发 Claude 插件 |
| **playwright** | E2E 测试 | 浏览器自动化测试 |
| **pr-review-toolkit** | PR 审查工具 | 审查 Pull Request |
| **ralph-loop** | Ralph 循环 | 代码重构 |
| **ralph-wiggum** | 代码转换 | 代码风格转换 |
| **security-guidance** | 安全指导 | 安全相关建议 |
| **serena** | Serena 助手 | AI 助手功能 |
| **supabase** | Supabase 集成 | 数据库/认证 |

### everything-claude-code 插件
> 第三方插件，提供额外能力

| 类型 | 数量 | 说明 |
|------|------|------|
| **Agents** | 11+ | architect, build-error-resolver, code-reviewer, security-reviewer, tdd-guide 等 |
| **Skills** | 9+ | backend-patterns, frontend-patterns, continuous-learning, eval-harness 等 |
| **Commands** | 15 | /tdd, /plan, /e2e, /build-fix, /refactor-clean, /learn, /checkpoint, /verify 等 |
| **Rules** | 8 | security, coding-style, testing, git-workflow, agents, performance, patterns, hooks |
| **Hooks** | 6 | PreToolUse, PostToolUse, SessionStart, SessionEnd, PreCompact, Stop |

---

### 平台级能力 (F:\claude-code\.claude\)

#### MCP 服务器 (2个)
| 名称 | 功能 | 何时使用 |
|------|------|----------|
| **searxng** | 网络搜索 | 查最新文档/技术 |
| **vision-mcp** | 图片识别分析 | 看设计稿/截图 |

#### Skills (16个)
| 名称 | 功能 | 何时使用 |
|------|------|----------|
| **brainstorming** | 头脑风暴 | 创建新功能前 |
| **writing-plans** | 编写实现计划 | 设计确认后 |
| **executing-plans** | 执行计划 | 计划确认后 |
| **test-driven-development** | TDD 测试驱动 | 实现功能/修 bug |
| **systematic-debugging** | 系统化调试 | 遇到 bug/test 失败 |
| **verification-before-completion** | 完成前验证 | 声称完成前 |
| **backend-patterns** | 后端架构模式 | Node.js/Express 后端 |
| **security-review** | 安全审查 | 处理敏感数据 |
| **design-check** | 设计检查 | 设计阶段检查 |
| **continuous-learning** | 持续学习 | 自动提取模式 |
| **subagent-driven-development** | 子代理驱动开发 | 复杂多步骤任务 |
| **verification-loop** | 验证循环 | 持续验证场景 |
| **finishing-a-development-branch** | 完成开发分支 | 分支合并/PR/清理 |
| **requesting-code-review** | 请求代码审查 | 完成任务/重大功能 |
| **receiving-code-review** | 接收代码审查 | 收到审查反馈 |
| **using-superpowers** | Superpowers 使用指南 | 了解框架 |

#### Agents (3个)
| 名称 | 功能 | 何时使用 |
|------|------|----------|
| **architect** | 架构设计 | 系统架构设计 |
| **build-error-resolver** | 构建错误修复 | 构建失败/类型错误 |
| **security-reviewer** | 安全审查 | 安全漏洞检测 |

#### Tools (2个)
| 名称 | 功能 | 何时使用 |
|------|------|----------|
| **superpowers** | 完整开发工作流 | 标准开发流程 |
| **OpenSpec** | 规范管理 | 需要规范提案 |

#### Hooks (来自 everything-claude-code)
| Hook 类型 | 功能 | 状态 |
|-----------|------|------|
| **PreToolUse** | 智能提醒（tmux、git push） | ✅ 已启用 |
| **PostToolUse** | 自动格式化、类型检查、console.log 警告 | ✅ 已启用 |
| **SessionStart** | 加载上一次上下文 | ✅ 已启用 |
| **SessionEnd** | 持久化会话状态、提取模式 | ✅ 已启用 |
| **PreCompact** | 压缩前保存状态 | ✅ 已启用 |
| **Stop** | 响应结束后检查 | ✅ 已启用 |

---

## 🎯 快速使用指南

### 我要 [搜索网络/查最新文档]
→ searxng MCP 自动启用

### 我要 [看图片/设计稿]
→ vision-mcp 自动启用

### 我要 [快速开发功能]
→ 使用 feature-dev 插件

### 我要 [设计 UI]
→ 使用 frontend-design 插件

### 我要 [审查代码]
→ 使用 code-review 插件

### 我要 [创建新功能]
1. 调用 `brainstorming` Skill
2. 调用 `writing-plans` Skill
3. 调用 `executing-plans` Skill

### 我要 [修复 bug]
1. 调用 `systematic-debugging` Skill
2. 修复后调用 `test-driven-development` Skill

### 我要 [理解代码]
→ 启动 Explore Agent (通过 Task 工具)

### 我要 [设计架构]
→ 启动 Plan Agent 或 architect Agent

### 我要 [修复构建错误]
→ 启动 build-error-resolver Agent

### 我要 [GitHub 操作]
→ 使用 github 插件（PR、Issue、仓库管理）

---

## 📂 配置文件位置

| 级别 | 类型 | 位置 |
|------|------|------|
| **系统级** | 插件 | `C:\Users\Administrator\.claude\plugins\` |
| **系统级** | Hooks | `C:\Users\Administrator\.claude\settings.json` |
| **系统级** | MCP | `C:\Users\Administrator\.claude.json` |
| **平台级** | MCP | `.mcp.json` |
| **平台级** | Skills | `.claude/skills/` |
| **平台级** | Agents | `.claude/agents/` |
| **平台级** | Tools | `tools/` |
| **平台级** | Hooks | `.claude/settings.json` |

---

## 🔄 能力层级

```
系统级 (C:\Users\Administrator\.claude\)
    ├── 22+ 个官方插件 ✅ 自动可用
    ├── everything-claude-code 插件 ✅ 已安装
    ├── 内置 Skills ✅ 自动可用
    ├── Hooks 配置 ✅ 已启用
    └── MCP 服务器（20+ 个）
        ↓ 继承
平台级 (F:\claude-code\.claude\)  ← 当前文档管理范围
    ├── 2 个 MCP 服务器
    ├── 16 个 Skills
    ├── 3 个 Agents
    ├── 2 个 Tools
    └── Hooks ✅ 已启用
        ↓ 继承
项目级 (F:\claude-code\项目X\.claude\)
    └── 项目特定能力
```

---

## 📝 维护记录

| 日期 | 动作 | 说明 |
|------|------|------|
| 2026-01-28 | 创建 | 初始化能力总览 |
| 2026-01-28 | 更新 | 补充系统级插件、Hooks、Agents |
| 2026-01-28 | 更新 | 安装 everything-claude-code，启用 Hooks |

---

> **说明**：
> - **系统级插件**由 Claude Code 官方提供，自动可用
> - **everything-claude-code** 是第三方插件，提供额外的 Agents、Skills、Commands、Rules、Hooks
> - **平台级能力**是你配置的，作用于所有在 F:\claude-code\ 下创建的项目
> - **Hooks** 已启用，提供自动化功能（格式化、类型检查、会话持久化等）
> - **Explore/Plan 等 Agents** 通过 Task 工具动态启动，未列在表格中
