# Superpowers & OpenSpec 使用指南

> **更新日期**：2026-01-19
> **状态**：已集成

---

## 🎯 概述

已安装两个强大的开发工具：

1. **Superpowers** - 完整的软件开发工作流程框架
2. **OpenSpec** - 规范管理和提案流程工具

---

## 📚 工具介绍

### Superpowers

**来源**：https://github.com/obra/superpowers

**功能**：提供完整的软件开发工作流程，包括：

| 技能 | 用途 |
|------|------|
| `brainstorming` | 在任何创造性工作前使用，通过对话细化需求 |
| `writing-plans` | 将工作分解为小任务（2-5分钟） |
| `executing-plans` | 批量执行计划任务 |
| `test-driven-development` | 强制执行 TDD：红-绿-重构 |
| `using-git-worktrees` | 创建隔离的工作空间 |
| `subagent-driven-development` | 子代理驱动的开发流程 |

**核心理念**：
- 系统化优于临时决策
- 技能优先于直接行动
- 小任务优于大任务
- 测试驱动优于猜测

---

### OpenSpec

**来源**：https://github.com/Tenas-AI/OpenSpec-Chinese

**功能**：规范管理和提案流程

**触发场景**：
- ✅ 提到规划或提案（proposal, spec, change, plan）
- ✅ 引入新功能、破坏性变更、架构调整
- ✅ 重要的性能或安全工作
- ✅ 需求模糊，需要权威规范

**流程**：
```
检查触发条件 → 打开 OpenSpec → 创建提案 → 等待审批 → 实施
```

---

## 🔄 工作流程

### 完整流程

```
┌─────────────────────────────────────────────────────────┐
│  用户请求任务                                         │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  检查相关技能          │
        │  (Superpowers)        │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  brainstorming        │  ← 细化需求
        │  writing-plans        │  ← 编写计划
        │  executing-plans      │  ← 执行实现
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  检查 OpenSpec 触发   │
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
      满足                   不满足
        │                       │
        ▼                       │
  使用 OpenSpec                │
  创建提案                     │
  等待审批                     │
        │                       │
        └───────────┬───────────┘
                    │
                    ▼
            完成任务 ✓
```

---

## 📖 使用示例

### 示例 1：添加新功能

**用户**："添加用户登录功能"

**AI 流程**：
1. 检查技能 → 调用 `brainstorming`
2. 提问细化需求
3. 展示分段设计
4. 保存设计文档
5. 检查 OpenSpec → 触发（新功能）
6. 打开 `openspec/AGENTS.md`
7. 创建 OpenSpec 提案
8. 等待审批
9. 审批通过 → 执行实现

### 示例 2：修复 Bug

**用户**："修复登录页面样式问题"

**AI 流程**：
1. 检查技能 → 可能不需要 `brainstorming`
2. 直接修复问题
3. OpenSpec → 不触发（小修复）

### 示例 3：架构重构

**用户**："重构数据库层"

**AI 流程**：
1. 检查技能 → 调用 `brainstorming`
2. 架构设计方案
3. 检查 OpenSpec → 触发（架构变更）
4. 创建 OpenSpec 提案
5. 等待审批（可能需要多次讨论）
6. 审批通过 → 执行 `writing-plans`
7. 执行 `executing-plans`

---

## 🎓 关键规则

### 规则 1：技能优先

```
IF 有1%可能性技能适用于任务
THEN 必须调用技能
```

**技能位置**：`F:\claude-code\tools\superpowers\skills\`

### 规则 2：OpenSpec 强制

```
IF 满足 OpenSpec 触发条件
THEN 必须使用 OpenSpec
```

**配置位置**：`F:\claude-code\openspec\AGENTS.md`

### 规则 3：文档记录

```
设计 → docs/plans/
提案 → openspec/proposals/
```

---

## 📂 重要文件位置

| 文件 | 位置 | 说明 |
|------|------|------|
| **AGENTS.md** | `F:\claude-code\AGENTS.md` | 工作流程规范 |
| **OpenSpec 配置** | `F:\claude-code\openspec\AGENTS.md` | OpenSpec 项目配置 |
| **Superpowers 技能** | `F:\claude-code\tools\superpowers\skills\` | 所有技能定义 |
| **OpenSpec 规范** | `F:\claude-code\tools\OpenSpec-Chinese\AGENTS.md` | OpenSpec 规范说明 |

---

## ⚙️ 安装状态

✅ **Superpowers** - 已克隆到 `F:\claude-code\tools\superpowers\`
✅ **OpenSpec** - 已克隆到 `F:\claude-code\tools\OpenSpec-Chinese\`
✅ **工作流程** - 已配置完成
✅ **OpenSpec 配置** - 已创建 `openspec/AGENTS.md`

---

## 🔗 相关链接

- [Superpowers GitHub](https://github.com/obra/superpowers)
- [OpenSpec GitHub](https://github.com/Tenas-AI/OpenSpec-Chinese)
- [工作流程规范](../AGENTS.md)

---

## 💡 下一步

1. 阅读 [AGENTS.md](../AGENTS.md) 了解完整工作流程
2. 查看 [Superpowers README](../tools/superpowers/README.md) 了解更多细节
3. 查看 [OpenSpec 配置](../openspec/AGENTS.md) 了解触发条件

---

> 💡 **提示**：这两个工具会显著提升开发效率和代码质量，建议花时间熟悉它们的工作方式！
