# 开发流程工具选择指南

> **用途**：帮助快速选择合适的开发工具
>
> **数据来源**：基于 TOOL-KNOWLEDGE 目录的实际测试验证结果

---

## 📊 工具评分概览

> ⭐⭐⭐⭐⭐ 强烈推荐 | ⭐⭐⭐ 中等推荐 | ⭐ 低分不推荐

| 工具 | 评分 | 类型 | 核心用途 |
|------|------|------|----------|
| **code-review** | 100/100 | Skill | 代码审查专家（主工具） |
| **test-driven-development** | 90.85% | Skill | TDD 测试驱动开发 |
| **chrome-devtools** | 91.25% | MCP | Web 自动化测试 |
| **brainstorming** | 85/100 | Skill | 问题分析和需求细化 |
| **security-review** | 76% | Skill | 安全检查清单 |
| **mcp__cclsp** | 73.6% | MCP | 代码导航（Serena 替代） |
| **backend-patterns** | 16.95/100 | Skill | ❌ 不推荐（已淘汰） |

---

## 🎯 快速决策树

```
收到开发任务
    │
    ├─ 类型判断
    │   │
    │   ├─ 【需求分析/问题诊断】
    │   │   └─> brainstorming ⭐⭐⭐⭐⭐ (85/100)
    │   │
    │   ├─ 【规范管理/提案审批】
    │   │   └─> OpenSpec
    │   │
    │   ├─ 【功能开发/代码实现】
    │   │   │
    │   │   ├─ TDD 开发 → test-driven-development ⭐⭐⭐⭐⭐
    │   │   ├─ 前端测试 → chrome-devtools ⭐⭐⭐⭐⭐
    │   │   ├─ 完整项目 → superpowers
    │   │   └─ 代码导航 → mcp__cclsp ⭐⭐⭐
    │   │
    │   ├─ 【代码审查/质量检查】
    │   │   └─> code-review ⭐⭐⭐⭐⭐ (100/100)
    │   │       └─ security-review ⭐⭐⭐⭐ (76%) 补充
    │   │
    │   └─ 【项目立项/可行性分析】
    │       └─> agent-skills (doc-organizer + business-analyst)
    │
    ▼
使用推荐工具 ✓
```

---

## 📋 工具对比表

### 按任务类型选择（基于测试评分）

| 任务类型 | 推荐工具 | 评分 | 调用方式 | 说明 |
|----------|----------|------|----------|------|
| **代码审查** | code-review | 100/100 | 自动技能 | ⭐⭐⭐⭐⭐ 主审查工具 |
| **TDD 开发** | test-driven-development | 90.85% | 自动技能 | ⭐⭐⭐⭐⭐ 测试驱动开发 |
| **前端测试** | chrome-devtools | 91.25% | MCP 工具 | ⭐⭐⭐⭐⭐ Web 自动化 |
| **需求分析** | brainstorming | 85/100 | 自动技能 | ⭐⭐⭐⭐⭐ 问题根因分析 |
| **安全检查** | security-review | 76% | 自动技能 | ⭐⭐⭐⭐ 安全清单 |
| **代码导航** | mcp__cclsp | 73.6% | MCP 工具 | ⭐⭐⭐ 符号查找 |
| **项目立项** | agent-skills | - | 自动技能 | 可行性分析流程 |
| **规范提案** | OpenSpec | - | 自动触发 | 规范管理工具 |
| **架构审查** | backend-patterns | 16.95/100 | ❌ | ❌ 不推荐使用 |

---

## 🛠️ 详细工具说明

### 1. code-review ⭐⭐⭐⭐⭐ - 代码审查专家

**评分**：100/100

**适用场景**：
- ✅ Pull Request 代码审查
- ✅ TypeScript 类型检查
- ✅ 安全漏洞识别
- ✅ 性能问题分析

**核心价值**：
- ✅ 深度代码分析（类型、规范、性能）
- ✅ 完美适配 Electron + React 项目
- ✅ 全面超越 backend-patterns

**位置**：`F:\claude-code\TOOL-KNOWLEDGE\evaluations\code-review-evaluation.md`

**使用方式**：自动技能调用

---

### 2. test-driven-development ⭐⭐⭐⭐⭐ - TDD 测试驱动

**评分**：90.85%

**适用场景**：
- ✅ 新功能开发（先写测试）
- ✅ Bug 修复（编写复现测试）
- ✅ 重构验证

**核心价值**：
- ✅ 严格遵循 TDD 原则
- ✅ 测试质量高（93%）
- ✅ Jest 集成完美

**位置**：`F:\claude-code\TOOL-KNOWLEDGE\evaluations\test-driven-development-evaluation.md`

**使用方式**：自动技能调用

---

### 3. chrome-devtools ⭐⭐⭐⭐⭐ - Web 自动化测试

**评分**：91.25%（Web 功能）

**适用场景**：
- ✅ React 组件测试
- ✅ UI 交互测试
- ✅ 控制台调试
- ✅ 网络监控

**核心价值**：
- ✅ React 组件测试专家
- ✅ 性能优异（248ms 响应）
- ✅ 易用性极佳

**⚠️ 限制**：Electron 适配待补充

**位置**：`F:\claude-code\TOOL-KNOWLEDGE\evaluations\chrome-devtools-evaluation.md`

**使用方式**：MCP 工具调用

---

### 4. brainstorming ⭐⭐⭐⭐⭐ - 问题分析专家

**评分**：85/100

**适用场景**：
- ✅ 新功能设计
- ✅ 复杂问题根因分析
- ✅ 架构规划

**核心价值**：
- ✅ 深入问题分析
- ✅ 多维度思考
- ✅ 测试通过率 100%

**位置**：`F:\claude-code\TOOL-KNOWLEDGE\evaluations\brainstorming-evaluation.md`

**使用方式**：自动技能调用

---

### 5. security-review ⭐⭐⭐⭐ - 安全检查清单

**评分**：76%（真阳性率 100%）

**适用场景**：
- ✅ 有安全经验的开发者
- ✅ Code Review 检查清单
- ✅ 安全编码实践参考

**核心价值**：
- ✅ 100% 真阳性率
- ✅ 发现 10 个真实安全问题
- ✅ OWASP Top 10 覆盖

**⚠️ 定位**：检查清单工具，非自动化扫描器

**位置**：`F:\claude-code\TOOL-KNOWLEDGE\evaluations\security-review-evaluation.md`

**使用方式**：自动技能调用

---

### 6. mcp__cclsp ⭐⭐⭐ - 代码导航工具

**评分**：73.6%

**适用场景**：
- ✅ 日常代码导航
- ✅ TypeScript 项目
- ✅ Electron 项目

**核心价值**：
- ✅ 符号定义查找优秀（100分）
- ✅ TypeScript 支持完美

**核心限制**：
- ⚠️ 引用查找有限（30分）
- ⚠️ 不支持 IPC 追踪

**位置**：`F:\claude-code\TOOL-KNOWLEDGE\evaluations\cclsp-evaluation.md`

**使用方式**：MCP 工具调用

---

### 7. backend-patterns ⭐ - 架构审查（已淘汰）

**评分**：16.95/100

**核心问题**：
- ❌ 参考文档系统，非代码分析工具
- ❌ 无法主动分析代码
- ❌ 不适合 Electron 项目

**强烈替代方案**：
- ✅ **code-review skill**（100/100）

**适用场景**：
- ⚠️ 仅适用于 Node.js 后端项目学习
- ❌ Electron 项目不推荐

**位置**：`F:\claude-code\TOOL-KNOWLEDGE\evaluations\backend-patterns-evaluation.md`

---

### 8. agent-skills - AI Agent 协作系统

**适用场景**：
- ✅ 项目立项可行性分析
- ✅ 产品需求分析
- ✅ 文档整理和结构化
- ✅ 从分析到玩法的完整流程

**核心技能**：
- `doc-organizer` - 文档整理者
- `business-analyst` - 商业分析师
- `devil-advocate` - 魔鬼代言人
- `social-game-designer` - 社交游戏设计师

**位置**：`F:\claude-code\agent-skills\skills\`

**使用方式**：自动技能调用

---

### 2. superpowers - 软件开发工作流程

**适用场景**：
- ✅ 完整的软件开发项目
- ✅ 需要系统化流程的复杂任务
- ✅ 强调 TDD 和代码质量

**核心技能**：
- `brainstorming` - 头脑风暴
- `writing-plans` - 编写计划
- `executing-plans` - 执行计划
- `test-driven-development` - TDD

**位置**：`F:\claude-code\tools\superpowers\skills\`

**使用方式**：自动技能调用

---

### 3. OpenSpec - 规范管理工具

**适用场景**：
- ✅ 重要变更需要规范
- ✅ 架构调整需要审批
- ✅ 需求模糊需要权威规范

**触发条件**：
- 规划或提案相关
- 新功能、破坏性变更
- 架构调整
- 重要性能/安全工作

**位置**：`F:\claude-code\openspec\AGENTS.md`

**使用方式**：自动触发检测

---

### 4. feature-dev - 功能开发引导

**适用场景**：
- ✅ 快速实现单个功能
- ✅ 理解现有代码库
- ✅ 中小型开发任务

**命令**：`/feature-dev`

**使用方式**：Claude Code Plugin 命令

---

### 5. frontend-design - 前端设计

**适用场景**：
- ✅ UI/UX 设计
- ✅ 前端组件开发
- ✅ 界面代码生成

**命令**：`/frontend-design`

**使用方式**：Claude Code Plugin 命令

---

### 6. code-review - 代码审查

**适用场景**：
- ✅ PR 代码审查
- ✅ 代码质量检查
- ✅ 改进建议提供

**命令**：`/code-review`

**使用方式**：Claude Code Plugin 命令

---

## 💡 使用建议

### 场景 1：新功能开发（TDD 流程）

```
用户："添加用户评论功能"

AI 检测 → 类型：功能开发
推荐 → test-driven-development ⭐⭐⭐⭐⭐

流程：
1. test-driven-development (先写测试)
2. 编写实现代码
3. code-review (审查代码) ⭐⭐⭐⭐⭐
4. chrome-devtools (UI 测试) ⭐⭐⭐⭐⭐
```

### 场景 2：问题诊断与修复

```
用户："这个 Bug 怎么修？"

AI 检测 → 类型：问题分析
推荐 → brainstorming ⭐⭐⭐⭐⭐

流程：
1. brainstorming (根因分析)
2. mcp__cclsp (代码导航) ⭐⭐⭐
3. test-driven-development (TDD 修复) ⭐⭐⭐⭐⭐
4. chrome-devtools (运行验证) ⭐⭐⭐⭐⭐
```

### 场景 3：代码质量保障

```
用户："审查这段代码"

AI 检测 → 类型：代码审查
推荐 → code-review ⭐⭐⭐⭐⭐

组合方案：
1. code-review (主审查工具) ⭐⭐⭐⭐⭐
2. security-review (安全补充) ⭐⭐⭐⭐
3. test-driven-development (测试覆盖) ⭐⭐⭐⭐⭐
```

### 场景 4：新项目立项

```
用户："我要做一个新项目"

AI 检测 → 类型：项目立项
推荐 → agent-skills

流程：
1. brainstorming (需求分析) ⭐⭐⭐⭐⭐
2. doc-organizer (文档整理)
3. business-analyst (商业分析)
4. devil-advocate (批判审查)
```

---

## 🚀 推荐组合方案（基于测试验证）

### 方案 1：Electron + React 项目标准流程

```
需求分析 → brainstorming ⭐⭐⭐⭐⭐
     ↓
TDD 开发 → test-driven-development ⭐⭐⭐⭐⭐
     ↓
代码导航 → mcp__cclsp ⭐⭐⭐
     ↓
代码审查 → code-review ⭐⭐⭐⭐⭐ + security-review ⭐⭐⭐⭐
     ↓
测试验证 → chrome-devtools ⭐⭐⭐⭐⭐
```

### 方案 2：代码质量保障三件套

```
┌─────────────────────────────────────┐
│  代码质量保障（均通过验证）           │
├─────────────────────────────────────┤
│  code-review ⭐⭐⭐⭐⭐ (100/100)     │
│  security-review ⭐⭐⭐⭐ (76%)        │
│  test-driven-development ⭐⭐⭐⭐⭐    │
└─────────────────────────────────────┘
```

### 方案 3：问题分析与调试完整流程

```
问题发现 → brainstorming ⭐⭐⭐⭐⭐ (根因分析)
     ↓
代码定位 → mcp__cclsp ⭐⭐⭐ (符号导航)
     ↓
问题修复 → test-driven-development ⭐⭐⭐⭐⭐ (TDD 修复)
     ↓
验证测试 → chrome-devtools ⭐⭐⭐⭐⭐ (运行验证)
     ↓
质量检查 → code-review ⭐⭐⭐⭐⭐ (最终审查)
```

---

## 🎯 快速命令参考

### Skill 自动调用（推荐）

```
# 高分工具会自动调用，优先级按评分排序
1. code-review ⭐⭐⭐⭐⭐ - 代码审查
2. test-driven-development ⭐⭐⭐⭐⭐ - TDD 开发
3. chrome-devtools ⭐⭐⭐⭐⭐ - Web 测试
4. brainstorming ⭐⭐⭐⭐⭐ - 问题分析
5. security-review ⭐⭐⭐⭐ - 安全检查
```

### MCP 工具调用

```
# 需要 MCP 配置
- mcp__cclsp - 代码导航
- chrome-devtools - 浏览器自动化
```

---

## 🔄 工具切换

```
┌─────────────────────────────────────────┐
│  需要特定工具？直接告诉 AI               │
│                                         │
│  示例：                                  │
│  "使用 code-review 审查这段代码"         │
│  "用 brainstorming 分析这个问题"         │
│  "调用 TDD 流程开发这个功能"             │
│  "用 chrome-devtools 测试这个组件"       │
└─────────────────────────────────────────┘
```

---

## 📊 决策流程图（更新版）

```
                    接收任务
                       │
                       ▼
              ┌──────────────────┐
              │  任务类型是什么？  │
              └────────┬─────────┘
                       │
       ┌───────────────┼───────────────┬─────────────┐
       │               │               │             │
   项目立项        问题分析        功能开发      代码审查
       │               │               │             │
       ▼               ▼               ▼             ▼
 agent-skills    brainstorming    test-driven   code-review
                       │           development    security-review
                       │               │         (100/100)
                       │               ▼             │
                       │         ┌─────┴────┐       │
                       │         │          │       │
                       │      后端        前端      │
                       │         │          │       │
                       │         │          ▼       │
                       │         │   chrome-devtools│
                       │         │      (91.25%)    │
                       │         │          │       │
                       └─────────┴──────────┴───────┘
                                   │
                                   ▼
                            完成任务 ✓
```

---

## 🔗 相关文档

### 测试验证报告
- [工具评估索引](../TOOL-KNOWLEDGE/TOOLS-INDEX.md) - 完整测试结果
- [工具对比总结](../TOOL-KNOWLEDGE/comparisons/tool-comparison-summary.md) - 详细对比
- [评估报告目录](../TOOL-KNOWLEDGE/evaluations/README.md) - 各工具详细评估

### 工作流程
- [AGENTS.md](../AGENTS.md) - 完整工作流程
- [CLAUDE.md](../CLAUDE.md) - 全局配置
- [Superpowers README](../tools/superpowers/README.md)

---

## 💬 交互提示

**对 AI 说**：
- "使用 code-review 审查这段代码"
- "用 TDD 流程开发这个功能"
- "用 brainstorming 分析这个问题"
- "调用 chrome-devtools 测试这个组件"
- "切换到 test-driven-development"

---

> 💡 **提示**：基于 TOOL-KNOWLEDGE 的实际测试验证，所有推荐工具都有详细的评估报告支持！

---
