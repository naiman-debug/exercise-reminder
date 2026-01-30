# 开发流程工具选择指南

> **用途**：帮助快速选择合适的开发工具

---

## 🎯 快速决策树

```
收到开发任务
    │
    ├─ 类型判断
    │   │
    │   ├─ 【需求分析/项目立项】
    │   │   └─> agent-skills (doc-organizer + business-analyst)
    │   │
    │   ├─ 【规范管理/提案审批】
    │   │   └─> OpenSpec
    │   │
    │   ├─ 【功能开发/代码实现】
    │   │   │
    │   │   ├─ 简单功能 → feature-dev
    │   │   ├─ 完整项目 → superpowers
    │   │   └─ 前端界面 → frontend-design
    │   │
    │   ├─ 【代码审查/质量检查】
    │   │   └─> code-review
    │   │
    │   └─ 【其他】
    │       └─> 根据具体需求判断
    │
    ▼
使用推荐工具 ✓
```

---

## 📋 工具对比表

### 按任务类型选择

| 任务类型 | 推荐工具 | 调用方式 | 说明 |
|----------|----------|----------|------|
| **需求分析** | agent-skills | 自动技能 | doc-organizer + business-analyst |
| **项目立项** | agent-skills | 自动技能 | 完整的可行性分析流程 |
| **规范提案** | OpenSpec | 自动触发 | 重要变更需要规范审批 |
| **简单功能** | feature-dev | `/feature-dev` | 快速实现单个功能 |
| **完整项目** | superpowers | 自动技能 | 系统化的开发流程 |
| **前端设计** | frontend-design | `/frontend-design` | UI/UX 设计和代码生成 |
| **代码审查** | code-review | `/code-review` | PR 代码审查 |

---

## 🛠️ 详细工具说明

### 1. agent-skills - AI Agent 协作系统

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

### 场景 1：新项目立项

```
用户："我要做一个社交游戏项目"

AI 检测 → 类型：项目立项
推荐 → agent-skills

流程：
1. doc-organizer (文档整理)
2. business-analyst (商业分析)
3. devil-advocate (批判审查)
4. social-game-designer (玩法设计)
```

### 场景 2：添加单个功能

```
用户："给这个项目添加用户评论功能"

AI 检测 → 类型：功能开发
推荐 → feature-dev

命令：/feature-dev
```

### 场景 3：完整项目重构

```
用户："重构这个项目的数据库层"

AI 检测 → 类型：重要变更
推荐 → superpowers + OpenSpec

流程：
1. OpenSpec (创建提案)
2. superpowers (执行开发)
```

### 场景 4：设计前端页面

```
用户："设计一个登录页面"

AI 检测 → 类型：前端设计
推荐 → frontend-design

命令：/frontend-design
```

---

## 🎯 快速命令参考

### Plugin 命令

```bash
# 功能开发
/feature-dev

# 前端设计
/frontend-design

# 代码审查
/code-review
```

### 技能调用

```
# 技能会自动调用，无需手动
# AI 会根据任务类型选择合适的技能
```

---

## 🔄 工具切换

```
┌─────────────────────────────────────────┐
│  当前任务不适合当前工具？               │
│                                         │
│  告诉 AI："切换到 [工具名称]"           │
│                                         │
│  示例：                                  │
│  "切换到 feature-dev"                    │
│  "使用 superpowers 流程"                 │
│  "调用 code-review"                     │
└─────────────────────────────────────────┘
```

---

## 📊 决策流程图

```
                    接收任务
                       │
                       ▼
              ┌──────────────────┐
              │  任务类型是什么？  │
              └────────┬─────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
   项目立项        规范提案        功能开发
       │               │               │
       ▼               ▼               ▼
 agent-skills     OpenSpec      ┌─────┴────┐
                                │          │
                            简单        复杂
                                │          │
                                ▼          ▼
                           feature-dev  superpowers
       │               │               │
       └───────────────┴───────────────┘
                       │
                       ▼
                   执行任务 ✓
```

---

## 🔗 相关文档

- [AGENTS.md](../AGENTS.md) - 完整工作流程
- [TOOLS_GUIDE.md](TOOLS_GUIDE.md) - 工具使用指南
- [Superpowers README](../tools/superpowers/README.md)
- [agent-skills README](../agent-skills/README.md)

---

## 💬 交互提示

**对 AI 说**：
- "帮我选择合适的工具"
- "这个任务应该用什么流程？"
- "切换到 [工具名称]"
- "对比一下这些工具的区别"

---

> 💡 **提示**：AI 会根据你的任务自动推荐合适的工具，你也可以手动指定使用哪个工具！
