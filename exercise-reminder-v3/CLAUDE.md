# 健康提醒助手 - AI 辅助开发配置

> 本文件定义项目级别的 Claude Code 辅助开发规范

---

## 📦 项目信息

**项目名称**：健康提醒助手 (Health Reminder)
**项目版本**：v3.0.0
**技术栈**：Electron 33 + React 18 + TypeScript 5
**开发工具**：Claude Code

---

## 🎯 项目特定配置

### 技术栈详情

```yaml
桌面框架: Electron 33+
前端框架: React 18
类型系统: TypeScript 5
构建工具: Vite 5
样式方案: Tailwind CSS 3
状态管理: Zustand
数据库: SQLite (better-sqlite3)
测试框架: Jest + React Testing Library
```

### 项目约束

| 约束项 | 目标值 | 说明 |
|--------|--------|------|
| **内存占用** | < 100MB | 运行时内存占用目标 |
| **启动时间** | < 2秒 | 应用冷启动时间 |
| **后台 CPU** | < 1% | 系统托盘时 CPU 占用 |
| **数据库查询** | < 1ms | SQLite 查询性能 |
| **测试覆盖率** | > 80% | 单元测试覆盖率目标 |

### 编码规范

- **TypeScript 严格模式**：启用所有严格检查
- **ESLint**：遵循 Airbnb 风格指南
- **Prettier**：统一代码格式化
- **Git Hooks**：Pre-commit 类型检查和格式化

---

## 🤖 AI Agent 工作流程

本项目遵循 [Claude Code 全局工作流程规范](../AGENTS.md)：

### 核心流程

```
1. 约束规则检查
   ↓
2. 技能调用 (Superpowers)
   ↓
3. 开发执行 (brainstorming → writing-plans → executing-plans)
   ↓
4. 规范检查 (重要变更需要 OpenSpec 提案)
   ↓
5. 工作日志 (更新 TASKS.md 和 CURRENT_TASK.md)
   ↓
6. 测试验证 (test-driven-development)
```

### 技能使用映射

| 开发阶段 | 使用技能 | 触发条件 |
|---------|---------|----------|
| **需求分析** | `brainstorming` | 功能开发前 |
| **计划制定** | `writing-plans` | 复杂功能实现前 |
| **代码执行** | `executing-plans` | 按计划编码 |
| **测试驱动** | `test-driven-development` | 所有功能开发 |
| **安全审查** | `security-review` | 处理用户输入、敏感数据 |
| **代码审查** | `requesting-code-review` | 完成重要模块后 |

---

## 📂 项目架构要点

### Electron 架构

```
主进程 (Main Process)
├── 提醒调度 (reminder/scheduler.ts)
│   └── 三个独立定时器，互不干扰
├── 数据库管理 (database/queries.ts)
│   └── SQLite 本地存储
├── IPC 通信 (ipc/handlers.ts)
│   └── 渲染进程与主进程通信
└── 系统托盘 (tray/)
    └── 右键菜单、暂停/恢复

渲染进程 (Renderer Process)
├── React 18 组件
├── Zustand 状态管理
└── Tailwind CSS 样式
```

### 核心业务逻辑

#### 三类独立提醒

```typescript
// 提醒类型独立运行，不共享时间线
type ReminderType = 'exercise' | 'gaze' | 'stand';

// 关键规则：
// 1. 各自独立运行
// 2. 不能同时触发（最小间隔 2 分钟）
// 3. 在设定范围内随机触发
```

#### MET 卡路里计算

```typescript
// 公式：消耗(大卡) = MET × 体重(kg) × 时长(分钟) / 60
function calculateCalories(
  metValue: number,
  weightKg: number,
  durationSeconds: number
): number
```

---

## 📁 文件组织规范

### 根目录文件（符合全局规范）

```
exercise-reminder-v3/
├── README.md          # 项目说明
├── CLAUDE.md          # 本文件 - AI 辅助配置
├── CURRENT_TASK.md    # 当前任务快照
└── docs/              # 详细文档
```

### 关键文档

| 文档 | 用途 |
|------|------|
| [健康提醒助手PRD_v2.md](./健康提醒助手PRD_v2.md) | 产品需求文档 |
| [健康提醒助手_技术方案.md](./健康提醒助手_技术方案.md) | 技术实现方案 |
| [docs/TASKS.md](./docs/TASKS.md) | 详细任务管理 |
| [docs/WORK-LOG.md](./docs/WORK-LOG.md) | 工作日志 |

### v2 历史参考

`bak/` 目录包含 v2 版本（Python + PySide6）的代码和设计，**仅供参考**：

- ⚠️ 不得直接复制 v2 代码
- ✅ 可以参考 `bak/prd.md` 了解原始需求
- ✅ 可以参考 `bak/tokens.py` 的设计规范
- ✅ 可以参考 `bak/dialogs/` 的交互逻辑

---

## 🧪 测试策略

### 测试层级

```
单元测试
├── 工具函数测试 (src/utils/__tests__)
├── Store 测试 (src/store/__tests__)
└── 组件测试 (src/pages/__tests__)

集成测试
├── IPC 通信测试 (electron/__tests__)
└── 数据库测试 (electron/database/__tests__)

E2E 测试
└── 完整用户流程（未来添加）
```

### 测试命令

```bash
npm test              # 运行所有测试
npm run test:watch    # 监听模式
npm run typecheck     # TypeScript 类型检查
```

---

## 🔗 全局配置引用

本项目遵循全局规范：

- **[全局 AGENTS.md](../AGENTS.md)** - AI Agent 工作流程规范
- **[全局 INFRA.md](../INFRA.md)** - MCP/Skill/Agent 管理总入口
- **[文件组织规范](../.global/rules/FILE_ORGANIZATION_RULES.md)** - 全局文件组织规则
- **[工具选择指南](../docs/TOOL_SELECTION_GUIDE.md)** - 开发工具选择

---

## 📋 开发注意事项

### 重要约束

1. **性能约束**：所有开发必须考虑性能目标
2. **类型安全**：不允许使用 `any`，必须正确定义类型
3. **测试先行**：使用 TDD 技能，先写测试再写实现
4. **文档同步**：重要变更需更新相关文档

### 特殊场景处理

- **系统休眠**：唤醒后重新计算定时器
- **弹窗冲突**：确保最小 2 分钟间隔
- **数据迁移**：数据库 Schema 变更需要迁移脚本

### Git 提交规范

```bash
# 提交前会自动触发 pre-commit hook
# 1. TypeScript 类型检查
# 2. Prettier 格式化
# 3. ESLint 检查

# 请确保所有检查通过后再提交
```

---

## 🎯 当前开发阶段

**当前版本**：v3.0.0（开发中）
**已完成**：
- ✅ 项目初始化
- ✅ 基础架构搭建
- ✅ 数据库 Schema 设计
- ✅ 提醒调度器架构

**进行中**：
- 🔄 UI 组件开发
- 🔄 功能集成

**下一步**：
- [ ] 完成首页统计界面
- [ ] 完成设置页面
- [ ] 集成测试

详见：[CURRENT_TASK.md](./CURRENT_TASK.md) | [docs/TASKS.md](./docs/TASKS.md)
