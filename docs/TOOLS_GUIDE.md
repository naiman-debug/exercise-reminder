# 工具框架总览

> **三大开发框架对比与选择**
> **更新日期**：2026-02-01

---

## 📋 目录

1. [框架对比](#框架对比)
2. [如何选择](#如何选择)
3. [快速导航](#快速导航)
4. [组合使用](#组合使用)

---

## 框架对比

### 三大开发框架

| 框架 | 定位 | 覆盖范围 | 评分 | 适用场景 |
|------|------|----------|------|----------|
| **BMAD** | 全栈工作流 | 产品→开发→测试 | ⭐⭐⭐⭐⭐ | 新产品/大功能 |
| **Superpowers** | 开发工作流 | 需求→代码→测试 | ⭐⭐⭐⭐⭐ | 具体开发任务 |
| **OpenSpec** | 规范管理 | 提案→审批→实施 | ⭐⭐⭐⭐ | 重要变更 |

### 详细对比表

| 维度 | BMAD | Superpowers | OpenSpec |
|------|------|-------------|----------|
| **产品规划** | ✅ PM Agent + PRD | ⚠️ brainstorming | ❌ 无 |
| **架构设计** | ✅ Architect Agent | ❌ 无 | ❌ 无 |
| **需求分析** | ✅ 全流程 | ✅ brainstorming | ❌ 无 |
| **开发执行** | ✅ Dev Agent | ✅ 完整流程 | ❌ 无 |
| **测试** | ✅ TEA 模块 | ✅ TDD | ❌ 无 |
| **游戏开发** | ✅ GDS 模块 | ❌ 无 | ❌ 无 |
| **规范审批** | ✅ 实施就绪检查 | ❌ 无 | ✅ 提案审批 |
| **输出物** | PRD + 架构 + 代码 | 代码 | 提案文档 |
| **触发方式** | 命令调用 | 命令/Skill | 自动检测 |
| **学习曲线** | 较陡 | 中等 | 较低 |

---

## 如何选择

### 决策树

```
你要做什么？
│
├─ 【新产品 / 大功能开发】
│   │
│   ├─ 需要产品规划？
│   │   ├─ 是 → BMAD (PM → Architect → Dev)
│   │   └─ 否 ↓
│   │
│   ├─ 需要架构设计？
│   │   ├─ 是 → BMAD (Architect Agent)
│   │   └─ 否 ↓
│   │
│   └─ 【游戏开发】
│       ├─ 是 → BMAD (GDS 模块)
│       └─ 否 → BMAD (BMM 模块)
│
├─ 【具体开发任务】
│   │
│   ├─ 完整功能开发
│   │   └─ Superpowers (brainstorming → writing-plans → executing)
│   │
│   ├─ Bug 修复
│   │   └─ Superpowers (systematic-debugging → TDD)
│   │
│   └─ 小修改
│       └─ 直接开发或 Superpowers (TDD)
│
└─ 【重要变更 / 架构调整】
    │
    └─ OpenSpec (提案 → 审批 → 实施)
```

### 典型场景

| 场景 | 推荐框架 | 理由 |
|------|---------|------|
| **新产品立项** | BMAD | 完整的产品开发流程 |
| **大功能开发** | BMAD | 需要 PRD 和架构设计 |
| **具体功能实现** | Superpowers | 快速执行开发任务 |
| **Bug 修复** | Superpowers | 系统化调试 + TDD |
| **架构重构** | OpenSpec + Superpowers | 需要审批 + 执行 |
| **游戏开发** | BMAD GDS | 专门的游戏开发流程 |
| **安全相关改动** | OpenSpec | 需要规范审批 |
| **测试框架搭建** | BMAD TEA | 测试架构和 CI/CD |

---

## 快速导航

### BMAD - 全栈工作流框架 📖

**详细手册**：[BMAD_MANUAL.md](BMAD_MANUAL.md)

**核心模块**：
- **BMM** - 软件开发全流程
- **BMB** - BMAD 构建器
- **CIS** - 创新套件
- **GDS** - 游戏开发套件
- **TEA** - 测试卓越架构

**核心工作流**：
```bash
/bmad-bmm-create-prd              # 创建 PRD
/bmad-bmm-create-architecture     # 创建架构
/bmad-bmm-create-epics-and-stories # 创建史诗和故事
/bmad-bmm-quick-dev               # 快速开发
```

**适用场景**：
- ✅ 新产品开发
- ✅ 大功能开发
- ✅ 游戏开发
- ✅ 需要产品规划和架构设计

---

### Superpowers - 开发工作流框架 📖

**详细手册**：[SUPERPOWERS_MANUAL.md](SUPERPOWERS_MANUAL.md)

**核心 Skills**：
- **brainstorming** - 需求分析（85/100 ⭐⭐⭐⭐⭐）
- **writing-plans** - 编写计划
- **executing-plans** - 执行计划
- **test-driven-development** - TDD（90.85% ⭐⭐⭐⭐⭐）
- **systematic-debugging** - 系统化调试

**核心命令**：
```bash
/plan "任务描述"    # 编写计划
/tdd "功能描述"     # TDD 开发
/build-fix          # 修复构建错误
```

**适用场景**：
- ✅ 具体功能开发
- ✅ Bug 修复
- ✅ 代码重构
- ✅ 测试驱动开发

---

### OpenSpec - 规范管理工具 📖

**详细手册**：[OPENSPEC_MANUAL.md](OPENSPEC_MANUAL.md)

**核心功能**：
- 提案管理
- 审批流程
- 规范文档
- 决策记录

**触发条件**：
- ✅ 规划或提案相关
- ✅ 重要变更（新功能、破坏性变更、架构调整）
- ✅ 需求模糊

**适用场景**：
- ✅ 重要变更审批
- ✅ 架构调整
- ✅ 需要规范管理

---

## 组合使用

### 推荐组合方案

#### 方案 1：新产品开发（完整流程）

```
BMAD → OpenSpec → Superpowers

1. BMAD (PM + Architect) - 产品规划和技术设计
2. OpenSpec - 重要变更审批（如需要）
3. Superpowers - 具体开发执行
```

**适用**：新产品、大功能、需要完整流程

---

#### 方案 2：快速开发（简化流程）

```
Superpowers

brainstorming → writing-plans → executing-plans → TDD
```

**适用**：已知需求的具体功能

---

#### 方案 3：游戏开发

```
BMAD GDS

1. 游戏简报 (Game Brief)
2. 游戏设计文档 (GDD)
3. 游戏架构 (Game Architecture)
4. Sprint 规划
5. 功能开发
6. 游戏测试
```

**适用**：Unity/Unreal/Godot 游戏项目

---

#### 方案 4：架构重构

```
OpenSpec + Superpowers

1. OpenSpec - 创建重构提案
2. 审批通过
3. Superpowers - 执行重构
```

**适用**：重要架构调整

---

### 协作关系

```
┌─────────────────────────────────────────────────────────┐
│  BMAD (产品层面)                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │ PM: 产品规划 → PRD                              │   │
│  │ Architect: 技术设计 → 架构文档                   │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ OpenSpec (规范层面)                              │   │
│  │ 重要变更 → 提案 → 审批 → 实施                   │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Superpowers (执行层面)                          │   │
│  │ brainstorming → planning → executing → TDD      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 工具选择指南

### 基于任务类型

| 任务类型 | 首选 | 备选 |
|----------|------|------|
| 新产品立项 | BMAD | - |
| 大功能开发 | BMAD | Superpowers |
| 具体功能实现 | Superpowers | BMAD quick-dev |
| Bug 修复 | Superpowers | - |
| 架构重构 | OpenSpec + Superpowers | BMAD Architect |
| 游戏开发 | BMAD GDS | - |
| 重要变更 | OpenSpec | - |

### 基于项目规模

| 项目规模 | 推荐框架 |
|----------|---------|
| 小型（< 1周） | Superpowers 或直接开发 |
| 中型（1-4周） | Superpowers |
| 大型（> 1月） | BMAD |
| 复杂产品 | BMAD + Superpowers |

### 基于团队规模

| 团队规模 | 推荐框架 |
|----------|---------|
| 个人开发者 | Superpowers |
| 小团队（2-5人） | BMAD + Superpowers |
| 大团队（5+人） | BMAD + OpenSpec + Superpowers |

---

## 相关文档

### 框架手册
- [BMAD 操作手册](BMAD_MANUAL.md) - 全栈工作流框架完整指南
- [Superpowers 操作手册](SUPERPOWERS_MANUAL.md) - 开发工作流完整指南
- [OpenSpec 操作手册](OPENSPEC_MANUAL.md) - 规范管理完整指南

### 工具指南
- [工具选择指南](TOOL_SELECTION_GUIDE.md) - 基于测试验证的工具选择
- [Plugin 使用指南](plugin/PLUGIN使用指南.md) - 最新插件使用方法
- [INFRA.md](../INFRA.md) - 平台能力总览

### 工作流程
- [AGENTS.md](../AGENTS.md) - AI Agent 工作流程规范

---

## 快速开始

### 新手推荐

1. **第一步**：阅读本总览，了解三大框架
2. **第二步**：根据任务选择合适的框架
3. **第三步**：阅读对应的详细手册
4. **第四步**：开始使用

### 快速参考

```
新产品/大功能  → [BMAD 手册](BMAD_MANUAL.md)
具体开发任务    → [Superpowers 手册](SUPERPOWERS_MANUAL.md)
重要变更审批    → [OpenSpec 手册](OPENSPEC_MANUAL.md)
工具选择        → [工具选择指南](TOOL_SELECTION_GUIDE.md)
```

---

> 💡 **提示**：三大框架各有侧重，根据任务选择合适的框架可以大大提升开发效率！
>
> 🌟 **核心原则**：
> - **产品层面**用 BMAD
> - **执行层面**用 Superpowers
> - **规范层面**用 OpenSpec
