# 约束文档目录

> **项目**：exercise-reminder-v3
> **用途**：存储项目开发过程中的约束和规范文档

---

## 📋 约束文档清单

### 必须遵守的约束

所有 AI Agent 在开发此项目时，必须遵守以下约束文档：

#### 0. 关键文档自动更新约束 ⭐⭐⭐ **最高优先级** 🆕

**文档**：[critical-docs-auto-update.md](./critical-docs-auto-update.md)

**作用**：
- 确保项目关键文档始终保持最新状态
- 保证文档之间的一致性和同步
- 防止文档过时导致的信息不对称

**关键文档**：
- **README.md** - 项目门面
- **CLAUDE.md** - AI 辅助配置
- **CURRENT_TASK.md** - 当前任务快照
- **docs/TASKS.md** - 详细任务管理

**强制规则**（由 Git Hook 自动执行）：
- ✅ **约束文件变更时**：Git pre-commit hook 自动检查是否同步了 TASKS.md + CURRENT_TASK.md
- ✅ **代码文件变更时**：Git pre-commit hook 要求确认已使用 Skill 进行代码审查
- ✅ **提交前**：自动运行类型检查 + 单元测试（100% 通过才能提交）
- ✅ **提交信息**：Git commit-msg hook 验证 Conventional Commits 格式
- ✅ **提交后**：Git post-commit hook 自动更新 WORK-LOG.md
- ✅ **推送前**：Git pre-push hook 检查保护分支 + 运行最终测试

**执行方式**：100% Git Hook 强制执行，无需 AI 记忆

**关联更新矩阵**：
| 变更类型 | README.md | CLAUDE.md | CURRENT_TASK.md | docs/TASKS.md |
|----------|-----------|-----------|-----------------|--------------|
| 完成任务 | - | - | ✅ 必须更新 | ✅ 必须更新 |
| 开始任务 | - | - | ✅ 必须更新 | ✅ 必须更新 |
| 技术栈变更 | ✅ 必须更新 | ✅ 必须更新 | - | - |
| 架构变更 | ✅ 必须更新 | ✅ 必须更新 | - | - |
| 里程碑完成 | ✅ 更新路线图 | - | ✅ 更新进度 | ✅ 更新进度 |

---

#### 1. 工作流恢复约束 ⭐ **最重要**

**文档**：[workflow-recovery.md](./workflow-recovery.md)

**作用**：
- 确保新会话能够快速恢复工作状态
- 避免重复工作，保持开发连续性

**强制规则**：
- ✅ 每次会话启动必须先读取 `docs/TASKS.md`（任务看板）
- ✅ 然后读取 `docs/WORK-LOG.md` 最后 20 行（历史记录）
- ✅ 优先展示"🟡 进行中"和"🔴 待开始"的任务
- ✅ 识别快速恢复命令："继续"/"恢复"/"continue"/"resume"/"next"/"下一步"/"接着来"
- ✅ 完成任何模块后立即更新 TASKS.md（移至已完成）和 WORK-LOG.md（归档）
- ✅ 更新必须包含：总体进度%、待开发清单
- ✅ **完成开发后强制测试验证**（规则 11）

**触发命令**：
```
继续 / 恢复 / continue / resume / next / 下一步 / 接着来
```

**恢复响应格式**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 当前任务状态 (来自 TASKS.md)

🟡 进行中 (1 个任务)
  [ ] P0: 任务名称 - 进度: XX%

🔴 待开始 (2 个任务)
  [ ] P0: 任务名称
  [ ] P1: 任务名称

🟠 等待条件 (1 个任务)
  [ ] P1: 任务名称
     └─ 阻塞: 阻塞原因

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
是否继续某个任务？
输入 "继续 [任务名]" 或输入其他指令
```

#### 2. 任务看板 ⭐ **新增**

**文档**：`../docs/TASKS.md`

**作用**：
- 跟踪未完成任务的状态和进度
- 管理待开始、进行中、等待条件的任务
- 快速了解"还有什么没做完"

**强制规则**：
- ✅ 每次会话启动必须先读取 TASKS.md
- ✅ 优先展示"🟡 进行中"和"🔴 待开始"的任务
- ✅ 任务状态变更时必须更新（待开始→进行中→等待条件→完成）
- ✅ 完成后移到"✅ 已完成"（保留最近 5 条），其余归档到 WORK-LOG.md

**状态定义**：
- 🔴 **待开始**：新任务，尚未开始
- 🟡 **进行中**：正在执行，显示进度
- 🟠 **等待条件**：被阻塞，需要外部条件（如等待反馈、API Key）
- ✅ **已完成**：任务完成，归档到 WORK-LOG.md

**优先级**：
- P0：最高优先级，阻塞其他任务
- P1：高优先级，重要但不紧急
- P2：中等优先级，可以延后

#### 3. 测试规则

**文档**：[testing-rules.md](./testing-rules.md)

**作用**：
- 确保所有代码经过充分测试验证
- 提高代码质量和稳定性

**强制规则**：
- ✅ 完成模块后必须执行测试验证
- ✅ 修复 bug 后必须验证修复
- ✅ 使用指定的测试 Skills
- ✅ 只有测试全部通过才能标记"完成"

**必须使用的测试 Skills**：
```
- test-driven-development (强制)
- security-review (安全相关)
- backend-patterns (后端代码)
- requesting-code-review (推荐)
```

**测试通过标准**：
- ✅ 所有单元测试通过（100%）
- ✅ 无 TypeScript 类型错误
- ✅ 无 ESLint 警告
- ✅ 安全审查通过（如适用）

#### 4. Git Hooks 规则 ⭐ **新增**

**文档**：`docs/GIT-HOOKS.md`

**作用**：
- 自动化代码质量检查
- 规范提交信息格式
- 自动更新工作日志

**配置的 Hooks**：

| Hook | 触发时机 | 检查内容 |
|------|----------|----------|
| **pre-commit** | 提交前 | 类型检查 + 单元测试 |
| **commit-msg** | 提交信息编辑后 | Conventional Commits 格式 |
| **post-commit** | 提交完成后 | 自动更新 WORK-LOG.md |
| **pre-push** | 推送前 | 保护分支检查 + 最终测试 |

**强制规则**：
- ✅ Pre-commit 检查（类型 + 测试）
- ✅ 提交信息符合 Conventional Commits
- ✅ 推送前通过保护分支检查

**提交信息规范**：`<type>(<scope>): <subject>`

允许的 type：`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

---

#### 5. Git 自动提交推送规则 ⭐ **新增**

**文档**：[GIT-AUTO-COMMIT.md](./GIT-AUTO-COMMIT.md)

**作用**：
- 确保代码及时备份到 GitHub，防止丢失
- 自动化提交流程

**强制规则**：
- ✅ 完成任何代码后必须执行 git add + git commit + git push
- ✅ 会话结束前检查并推送未提交的修改
- ✅ 意外关闭后新会话检查未提交修改

**提交信息规范**：`<type>: <描述>`

允许的 type：`feat`, `fix`, `docs`, `style`, `test`, `chore`, `perf`, `ci`

---

#### 6. Hookify 自动提醒 ⭐ **新增**

**文档**：`.claude/hookify.*.local.md`

**作用**：
- 自动提醒 AI Agent 更新任务看板和工作日志
- 减少遗漏，确保工作记录完整

**规则列表**：

| 规则文件 | 触发事件 | 提醒内容 |
|----------|----------|----------|
| `hookify.task-check-session-end.local.md` | 会话结束 | 检查 TASKS.md 进行中任务 |
| `hookify.task-check-git-commit.local.md` | Git commit | 提醒更新任务状态 |
| `hookify.task-completion-reminder.local.md` | 检测完成关键词 | 提醒归档到 WORK-LOG.md |

**禁用方法**：
```bash
# 编辑对应文件，将 enabled: true 改为 enabled: false
# 或删除文件永久禁用
```

---

## 🎯 使用流程

### 新会话启动时

```
1. 读取 constraints/workflow-recovery.md
2. 读取 docs/WORK-LOG.md 最后 20 行
3. 按照恢复格式汇报当前状态
4. 等待用户确认
```

### 完成任务后

```
1. 执行强制测试验证
   ├─ 调用 test-driven-development skill
   ├─ 根据模块类型调用其他审查 skills
   └─ 运行所有测试

2. 验证测试通过
   ├─ 检查测试结果
   ├─ 生成测试报告
   └─ 修复问题（如有）

3. 更新 docs/WORK-LOG.md
```

---

## 📝 约束文档版本

- **v2.0** (2026-02-01) - 所有约束转换为 Git Hook 强制执行 🆕⭐⭐
  - **执行率从 40% 提升到 100%**
  - **pre-commit hook** 增强（4 项强制检查）：
    1. 关键文档同步检查（约束文件变更时必须同步 TASKS.md + CURRENT_TASK.md）
    2. 代码审查提醒（代码文件变更时确认已使用 Skill 审查）
    3. TypeScript 类型检查
    4. 单元测试验证（100% 通过）
  - **post-commit hook** 增强：
    - 自动更新 WORK-LOG.md
    - 约束文件变更提醒
  - **commit-msg hook**：
    - Conventional Commits 格式验证
  - **pre-push hook**：
    - 保护分支检查
    - 最终测试验证
  - **不再依赖 AI 主动遵守** - 全部通过 Git Hook 强制执行

- **v1.7** (2026-02-01) - 添加约束体系总览和自动更新检测
  - 新增 `constraints/critical-docs-auto-update.md` 文档
  - 定义 4 个关键文档（README.md、CLAUDE.md、CURRENT_TASK.md、docs/TASKS.md）
  - 创建关联更新矩阵（变更类型 → 受影响文档）
  - 新增 3 个 Hookify 规则：
    - `hookify.task-sync-on-complete.local.md` - 任务完成自动同步
    - `hookify.tech-stack-sync.local.md` - 技术栈变更自动关联
    - `hookify.doc-consistency-check.local.md` - 会话结束前一致性检查
  - 建立文档一致性验证机制

- **v1.5** (2026-02-01) - 添加 Git 自动提交推送规则 🆕
  - 新增 `constraints/GIT-AUTO-COMMIT.md` 文档
  - 新增 Hookify 规则 `hookify.git-auto-push.local.md`
  - 定义自动提交流程和错误处理方案

- **v1.4** (2026-02-01) - 添加 Git Hooks 规则 🆕
  - 新增 `docs/GIT-HOOKS.md` 文档
  - 配置 commit-msg（Conventional Commits 检查）
  - 配置 post-commit（自动更新工作日志）
  - 配置 pre-push（保护分支检查）
  - 更新 pre-commit（改进输出格式）

- **v1.3** (2026-02-01) - 添加 Hookify 自动提醒 🆕
  - 新增 3 个 Hookify 规则
  - 会话结束检查
  - Git commit 检查
  - 任务完成提醒

- **v1.2** (2026-02-01) - 添加任务看板机制 🆕
  - 新增 TASKS.md 任务看板
  - 更新工作流恢复约束（优先读取 TASKS.md）
  - 明确记录阈值（避免过度记录）
  - 添加任务状态管理规则

- **v1.1** (2026-01-30) - 添加测试规则文档
  - 新增 testing-rules.md
  - 更新工作流恢复约束（规则 11：强制测试）
  - 更新使用流程包含测试验证步骤

- **v1.0** (2026-01-30) - 初始版本
  - 添加工作流恢复约束
  - 定义 10 条核心规则

---

## 🔗 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| **任务看板** | `docs/TASKS.md` | 未完成任务跟踪 |
| **工作日志** | `docs/WORK-LOG.md` | 已完成工作归档 |
| **日志改进方案** | `docs/WORK-LOG-REDESIGN.md` | 设计方案文档 |
| **工作流程规范** | `F:\claude-code\AGENTS.md` | 平台级规范 |
| **项目配置** | `../CLAUDE.md` | 项目级配置 |

---

> ⚠️ **重要提示**：这些约束是强制性的，不是可选项！
>
> 所有 AI Agent 必须首先阅读并遵守这些约束，然后再开始开发工作。
