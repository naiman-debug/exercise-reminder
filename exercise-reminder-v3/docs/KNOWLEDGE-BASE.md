# 项目知识库

> exercise-reminder-v3 项目核心知识库
> 记录关键决策、技术选型、最佳实践和经验教训

---

## 📋 目录

1. [技术选型决策](#技术选型决策)
2. [架构设计决策](#架构设计决策)
3. [开发模式总结](#开发模式总结)
4. [Skills 使用经验](#skills-使用经验)
5. [MCP 工具使用经验](#mcp-工具使用经验)
6. [约束系统设计](#约束系统设计)
7. [成功案例](#成功案例)

---

## 技术选型决策

### 为什么选择 Electron + React + TypeScript？

| 方案 | 优势 | 劣势 | 最终选择 |
|------|------|------|----------|
| **Python + PySide6** (v2) | - 成熟的桌面框架<br>- 直接访问系统资源 | - 打包体积大<br>- UI 开发效率低 | ❌ 已废弃 |
| **Electron + React** | - 生态成熟<br>- 热重载开发<br>- 组件化开发 | - 内存占用较高 | ✅ **v3 采用** |
| **Tauri + React** | - 体积更小<br>- Rust 后端 | - 生态较新<br>- 学习曲线陡 | ⏸️ 未来考虑 |

**决策依据**：
- v2 使用 PySide6 开发效率低
- React 组件化开发更快速
- TypeScript 类型安全减少 bug
- 丰富的 UI 组件库（Tailwind CSS）

### 为什么选择 Zustand 而非 Redux？

| 对比项 | Zustand | Redux |
|--------|---------|-------|
| **代码量** | 极少 | 大量样板代码 |
| **学习曲线** | 平缓 | 陡峭 |
| **性能** | 优秀 | 优秀 |
| **中间件** | 内置 | 需额外配置 |
| **TypeScript** | 原生支持 | 需要额外类型定义 |

**决策**：Zustand ✅

### 为什么选择 better-sqlite3 而非 Prisma？

| 对比项 | better-sqlite3 | Prisma |
|--------|----------------|--------|
| **性能** | 同步 API，极快 | 异步 ORM，有开销 |
| **类型安全** | 需手写类型 | 自动生成类型 |
| **学习成本** | 低 SQL 知识 | 需学习 Prisma 语法 |
| **包大小** | 小 | 大 |
| **桌面应用适配** | 完美 | 过于重量级 |

**决策**：better-sqlite3 ✅

---

## 架构设计决策

### 主进程架构

```
main.ts (入口)
├── Database (数据库层)
│   ├── schema.ts (类型定义)
│   ├── db.ts (连接和初始化)
│   └── queries.ts (查询类)
├── IPC (通信层)
│   ├── channels.ts (通道常量)
│   ├── handlers.ts (处理器)
│   └── preload.ts (preload 脚本)
├── Reminder (提醒系统)
│   ├── scheduler.ts (调度器)
│   ├── timeline.ts (时间线)
│   └── reminder-window.ts (窗口管理)
└── Tray (系统托盘)
    └── tray.ts (托盘管理)
```

**关键设计决策**：

1. **单一职责原则**：每个模块只负责一个功能
2. **依赖注入**：Scheduler 通过构造函数注入 DatabaseQueries
3. **回调模式**：Timeline 通过回调通知触发事件

### 前端状态管理架构

```
Zustand Stores
├── useUserStore (用户信息)
├── useActivityStore (活动记录)
├── useSettingsStore (提醒设置)
├── useStatsStore (统计数据)
└── useExerciseStore (运动库)
```

**设计原则**：
- 按功能域拆分 store
- 每个 store 独立，避免循环依赖
- 统一错误处理模式

---

## 开发模式总结

### 初始阶段的问题

1. **混乱开发**：没有约束，随意创建文件
2. **上下文爆炸**：AI 会话越来越长，响应变慢
3. **测试缺失**：没有单元测试，bug 频发
4. **重复工作**：每次重启会话都要重新了解项目

### 约束驱动的开发模式

**核心思想**：通过约束文档引导 AI 行为

```
约束系统
├── FILE_ORGANIZATION_RULES.md (文件组织规则)
├── workflow-recovery.md (工作流恢复规则)
└── README.md (项目配置)
```

**效果**：
- ✅ 文件位置统一，不会随意创建
- ✅ 会话恢复快速，从 WORK-LOG.md 了解进度
- ✅ 上下文可控，强制压缩避免爆炸

---

## Skills 使用经验

### brainstorming

**使用场景**：新功能设计、需求细化

**经验**：
- ✅ 适合规划阶段，不紧急的任务
- ❌ 调试现有问题时会浪费时间
- **最佳实践**：先用 brainstorming 理清思路，再用 executing-plans 执行

### test-driven-development

**使用场景**：新功能开发、bug 修复

**经验**：
- ✅ 写测试前必须看测试失败
- ✅ 测试驱动能发现设计问题
- ❌ 现有代码添加测试不是真正的 TDD
- **最佳实践**：新功能严格 TDD，现有代码添加测试覆盖

### security-review

**使用场景**：处理用户输入、敏感数据

**经验**：
- ✅ 在开发阶段就发现安全问题
- ✅ 提供详细的修复建议
- **关键检查项**：输入验证、SQL 注入、XSS、认证

### backend-patterns

**使用场景**：后端架构设计、性能优化

**经验**：
- ✅ 提供成熟的架构模式
- ✅ 帮助发现潜在 bug
- **关键模式**：Repository、Service Layer、Caching

### feature-dev 系列

**使用场景**：复杂功能开发

**feature-dev:code-explorer** - 快速理解代码库
**feature-dev:code-architect** - 设计功能架构
**feature-dev:code-reviewer** - 代码审查

**经验**：
- ✅ 快速定位相关代码
- ✅ 提供架构级别的建议
- **最佳实践**：先用 explorer 了解，再用 architect 设计

---

## MCP 工具使用经验

### cclsp (Code Companion LSP)

**功能**：代码导航、查找定义、查找引用

**使用场景**：
- 快速定位函数定义
- 查找所有调用点
- 重构时分析影响范围

**经验**：
- ✅ 比 Grep 更精确，理解语义
- ✅ 结合 IDE 使用效果最佳

### filesystem

**功能**：文件操作（读写、搜索）

**使用场景**：
- 批量修改文件
- 搜索特定内容
- 目录结构分析

**经验**：
- ✅ 比 Bash 更安全，有权限检查
- ⚠️ 大文件读取注意性能

### playwright / chrome-devtools

**功能**：浏览器自动化、UI 测试

**使用场景**：
- 自动化截图
- UI 验证
- 性能分析

**经验**：
- ✅ 可验证实际渲染效果
- ⚠️ 需要等待页面加载

### pencil (设计系统)

**功能**：.pen 文件设计工具

**使用场景**：
- UI 设计
- 设计系统管理

**经验**：
- ⚠️ 本项目未使用，采用了 HTML 原型
- **替代方案**：直接 HTML + Tailwind 更快

---

## 约束系统设计

### 为什么需要约束文档？

**问题**：AI 在长时间对话中会：
1. 忘记之前的约定
2. 偏离项目结构
3. 重复犯同样的错误
4. 无法快速恢复工作状态

**解决方案**：将"如何工作"文档化

### workflow-recovery.md 设计经验

**触发条件**：用户输入"继续"、"恢复"等关键词

**核心规则**：
1. 读取 WORK-LOG.md 最后 20 行
2. 解析当前进度和下一步任务
3. 显示格式化恢复信息
4. 等待用户确认

**关键设计**：
- **上下文压缩规则**：完成模块/文件修改/阅读大量文档后必须执行 `/compact`
- **日志更新触发点**：完成模块、暂停任务、重要决策后必须更新 WORK-LOG.md

**效果**：
- ✅ 新会话 30 秒内恢复上下文
- ✅ 避免重复工作
- ✅ 保持开发连续性

### FILE_ORGANIZATION_RULES.md 设计经验

**核心原则**：
- 🚫 禁止随意在项目根目录创建文件
- 📂 所有文件必须有明确的归属目录
- 📦 不确定归属时使用临时目录 `temp/inbox/`

**决策树**：
```
要创建文件？
  ├─ 知道放哪里 → 放入对应目录
  └─ 不确定 → temp/inbox/ (之后再整理)
```

**效果**：
- ✅ 项目结构清晰
- ✅ 文件易于查找
- ✅ 减少重构时的文件移动

---

## 成功案例

### 案例 1：用 design-validator.ts 验证 UI

**背景**：创建了 HTML 原型但不确定是否符合设计规范

**工具**：.claude/scripts/design-verify.js

**流程**：
1. 为每个原型页面创建验证脚本
2. 使用 Playwright MCP 截图
3. 对比设计规范（颜色、间距、字体）
4. 生成验证报告

**结果**：
- ✅ 发现 12 处设计偏差
- ✅ 统一修正所有页面
- ✅ 确保 UI 一致性

**经验**：自动化验证 > 人工检查

### 案例 2：用 Skills 系统解决空白页面问题

**背景**：设置页面和运动库页面显示空白

**问题**：手动排查效率低，容易遗漏

**解决方案**：使用三个 Skills 并行审查
1. **test-driven-development** - 编写测试发现 API 调用失败
2. **security-review** - 检查输入验证和 IPC 安全
3. **backend-patterns** - 审查架构和潜在 bug

**发现**：
- P0: main.ts 未初始化关键模块
- P0: 数据库列名不匹配（snake_case vs camelCase）

**结果**：15 分钟定位并修复核心问题

**经验**：专业工具 > 手动排查

### 案例 3：WORK-LOG.md 工作流恢复

**背景**：多日开发，每次重启都要重新了解进度

**解决方案**：
- 每次完成任务后更新 WORK-LOG.md
- 记录完成内容、待开发部分、当前进度
- 使用 workflow-recovery.md 规则自动恢复

**效果**：
- 新会话 30 秒内恢复上下文
- 避免重复工作
- 保持开发连续性

**经验**：文档化进度 > 依赖记忆

---

## 经验教训

### 1. 数据库列名问题

**问题**：SQLite 使用 snake_case（`interval_min`），TypeScript 使用 camelCase（`intervalMin`）

**错误做法**：
```typescript
// 直接类型断言，字段不匹配
return this.db.prepare('SELECT * FROM reminder_settings').all() as ReminderSettings[];
```

**正确做法**：
```typescript
// 添加列名别名
return this.db.prepare(`
  SELECT
    id, type,
    interval_min as intervalMin,
    interval_max as intervalMax,
    duration,
    enabled,
    updated_at as updatedAt
  FROM reminder_settings
`).all() as ReminderSettings[];
```

**教训**：永远不要用 `SELECT *` + 类型断言

### 2. 主进程初始化顺序

**问题**：main.ts 没有初始化数据库、IPC 处理器、调度器

**错误代码**：
```typescript
app.whenReady().then(createWindow);
```

**正确代码**：
```typescript
app.whenReady().then(() => {
  createWindow();

  // 正确顺序
  const db = getDatabase();           // 1. 数据库
  const queries = new DatabaseQueries(db);
  scheduler = new ReminderScheduler(queries, () => mainWindow);
  registerIPCHandlers(scheduler);     // 2. IPC
  scheduler.start();                   // 3. 调度器
  registerTray(mainWindow, scheduler); // 4. 托盘
});
```

**教训**：Electron 应用启动时必须按正确顺序初始化所有模块

### 3. 状态管理缺少加载状态

**问题**：Settings 页面直接 map 空数组，无加载提示

**错误代码**：
```typescript
{reminderSettings.map((setting) => (...))}
```

**正确代码**：
```typescript
{isLoading && <div>加载中...</div>}
{error && <div>错误: {error}</div>}
{!isLoading && reminderSettings.map((setting) => (...))}
```

**教训**：异步状态必须处理加载和错误状态

---

## 技术债务清单

### 高优先级

- [ ] 添加用户输入验证（Zod）
- [ ] 添加 Error Boundary
- [ ] 完善错误处理机制
- [ ] 添加单元测试覆盖

### 中优先级

- [ ] 迁移到 Tauri（减小体积）
- [ ] 实现设置窗口独立窗口
- [ ] 添加数据导入/导出功能

### 低优先级

- [ ] 添加主题切换功能
- [ ] 添加多语言支持
- [ ] 优化数据库查询性能

---

## 更新记录

| 日期 | 内容 | 作者 |
|------|------|------|
| 2026-01-30 | 初始创建，记录技术选型和架构决策 | Claude Code |

---

> **规则**：每次遇到新问题或学到新经验后，必须立即更新本文档
