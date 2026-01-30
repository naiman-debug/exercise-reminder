# AGENTS.md - AI Agent 工作流程规范

> **工作目录**：F:\claude-code\
> **更新日期**：2026-01-19

---

## 🎯 核心工作流程

所有开发任务必须遵循以下流程：

```
┌─────────────────────────────────────────────────────────┐
│  1. 任务接收                                           │
│     └─> 调用 choose-tool 技能                          │
│         └─> 分析任务类型                                │
│         └─> 推荐合适工具                                │
│                                                         │
│  2. 工具执行                                           │
│     ├─ superpowers      (完整开发)                     │
│     ├─ OpenSpec         (规范提案)                     │
│     ├─ feature-dev      (快速开发)                     │
│     ├─ frontend-design  (前端设计)                     │
│     └─ code-review      (代码审查)                     │
│                                                         │
│  3. OpenSpec 检查（如适用）                            │
│     └─> 若满足触发条件，使用规范流程                    │
│                                                         │
│  4. 更新工作日志 ⭐ **新增**                           │
│     └─> 在项目 docs/WORK-LOG.md 中记录：               │
│         - 完成的任务和文件                              │
│         - 使用的技术和方法                              │
│         - 遇到的问题和解决方案                          │
│         - 下一步计划                                    │
│         - 当前进度总览                                  │
│                                                         │
│  5. 完成任务                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 第一步：工具选择与约束检查

### 1.1 阅读约束文档 ⭐ **重要**

在执行任何任务前，必须先检查并阅读项目约束文档。

**约束文档位置**：`{项目目录}/constraints/`

**必须阅读的约束**：
- `workflow-recovery.md` - 工作流恢复约束（最重要）
- `README.md` - 约束文档清单

**工作流恢复规则**：
```
1. 检查是否有 constraints/workflow-recovery.md
2. 如果有，读取 docs/WORK-LOG.md 最后 20 行
3. 识别快速恢复命令（"继续"/"恢复"/"continue"/"resume"等）
4. 按照恢复格式汇报当前状态
```

**恢复响应格式**：
```
[工作状态恢复]
📌 最后完成：[模块名]
📋 下一步：[待开发首项]
🛠️ 工具：[MCP/Skills]
📊 当前进度：[X]%
是否继续？
```

### 1.2 调用 choose-tool 技能

**技能位置**：`F:\claude-code\.global\skills\choose-tool\`

**功能**：分析任务并自动推荐最合适的工具

**可用工具**：
- `superpowers` - 完整的软件开发工作流程
- `OpenSpec` - 规范管理和提案流程
- `feature-dev` - 快速功能开发（Plugin）
- `frontend-design` - 前端界面设计（Plugin）
- `code-review` - 代码审查（Plugin）

**快速决策**：详见 [工具选择指南](docs/TOOL_SELECTION_GUIDE.md)

---

## 📋 第二步：工具执行

根据 choose-tool 的推荐，执行相应的工具或流程。

**技能位置**：`F:\claude-code\tools\superpowers\skills\`

**必须检查的技能**：
- `using-superpowers` - 如何使用技能系统
- `brainstorming` - 创意工作前的头脑风暴
- `writing-plans` - 编写实现计划
- `executing-plans` - 执行计划
- `test-driven-development` - TDD 测试驱动开发

**规则**：
```
┌─────────────────────────────────────────┐
│  IF 有1%可能性技能适用于任务             │
│    THEN 必须调用技能                     │
│                                         │
│  这不是可选项，是强制要求！              │
└─────────────────────────────────────────┘
```

---

## 🚀 第三步：superpowers 技能流程

### 3.1 brainstorming（头脑风暴）

**触发条件**：任何创造性工作
- 创建新功能
- 构建组件
- 添加功能
- 修改行为

**执行内容**：
1. 理解项目上下文
2. 通过提问细化想法
3. 探索不同方案
4. 分段展示设计
5. 保存设计文档

**输出**：`docs/plans/YYYY-MM-DD-<topic>-design.md`

### 3.2 writing-plans（编写计划）

**触发条件**：设计确认后

**执行内容**：
1. 将工作分解为小任务（2-5分钟每个）
2. 每个任务包含精确路径、完整代码、验证步骤
3. 强调 TDD、YAGNI、DRY 原则

**输出**：详细实现计划

### 3.3 executing-plans（执行计划）

**触发条件**：计划确认后

**执行内容**：
1. 批量执行计划任务
2. 每个任务后进行人工检查点
3. 代码审查
4. 测试验证

**输出**：完成的代码和测试

---

## 📐 第四步：OpenSpec 触发检查

在 superpowers 流程中或完成后，检查是否满足 OpenSpec 触发条件。

### 4.1 OpenSpec 触发条件

当请求涉及以下内容时，**必须**使用 OpenSpec：

- ✅ 提到规划或提案（proposal, spec, change, plan）
- ✅ 引入新功能、破坏性变更、架构转变
- ✅ 重要的性能或安全工作
- ✅ 需求模糊，需要权威规范才能编码

### 4.2 OpenSpec 使用流程

**触发后执行**：

1. **打开 OpenSpec 规范**
   ```
   打开文件：F:\claude-code\openspec\AGENTS.md
   ```

2. **遵循规范创建提案**
   - 使用 OpenSpec 格式
   - 遵循项目约定
   - 提交变更提案

3. **等待审批**
   - 提案需经审批
   - 审批通过后继续实现

**OpenSpec 位置**：`F:\claude-code\tools\OpenSpec-Chinese\`

---

## 📂 目录结构

```
F:\claude-code\
├── AGENTS.md                      # 本文件 - 工作流程规范
├── claude.md                      # 全局配置
│
├── tools/                         # 工具目录
│   ├── superpowers/               # Superpowers 框架
│   │   ├── skills/                # 技能库
│   │   │   ├── using-superpowers/
│   │   │   ├── brainstorming/
│   │   │   ├── writing-plans/
│   │   │   ├── executing-plans/
│   │   │   └── ...
│   │   └── README.md
│   │
│   └── OpenSpec-Chinese/          # OpenSpec 工具
│       ├── AGENTS.md              # OpenSpec 规范
│       ├── openspec/              # OpenSpec 核心
│       └── README.md
│
├── openspec/                      # OpenSpec 项目配置（待创建）
│   └── AGENTS.md                  # 项目级 OpenSpec 配置
│
└── {项目目录}/                    # 具体项目
    └── ...
```

---

## 🔄 完整工作流程示例

### 场景：添加新功能

```
1. 用户请求："添加用户登录功能"
   │
2. 检查技能 → 调用 brainstorming
   │
3. 头脑风暴 → 提问细化需求
   │
4. 展示设计 → 用户确认
   │
5. 保存设计文档
   │
6. 调用 writing-plans → 创建实现计划
   │
7. 检查：是否需要 OpenSpec？
   ├─ 是 → 打开 openspec/AGENTS.md → 创建提案 → 等待审批
   └─ 否 → 继续
   │
8. 调用 executing-plans → 执行实现
   │
9. 完成 → 测试 → 提交
   │
10. 更新工作日志 ⭐ **新增**
    └─> 在项目 docs/WORK-LOG.md 中记录：
        - 完成的功能
        - 创建的文件
        - 使用的技术
        - 遇到的问题
        - 下一步计划
```

### 场景：架构变更

```
1. 用户请求："重构数据库层"
   │
2. 检查技能 → 调用 brainstorming
   │
3. 头脑风暴 → 架构设计方案
   │
4. 检查：是否需要 OpenSpec？
   ✅ 是（架构变更）
   │
5. 打开 openspec/AGENTS.md
   │
6. 创建 OpenSpec 提案
   │
7. 等待审批
   │
8. 审批通过 → 执行 superpowers 流程
   │
9. 实现 → 测试 → 提交
   │
10. 更新工作日志 ⭐ **新增**
    └─> 在项目 docs/WORK-LOG.md 中记录：
        - 架构变更内容
        - 实现步骤
        - 影响范围
        - 下一步计划
```

---

## ⚠️ 重要规则

### 规则 1：技能优先

```
在任何响应或行动之前，必须先检查并调用相关技能！
即使是简单的澄清问题，也要先检查技能。
```

### 规则 2：OpenSpec 强制触发

```
如果满足 OpenSpec 触发条件，必须使用 OpenSpec！
不能跳过，不能走捷径！
```

### 规则 3：文档记录

```
所有设计和计划必须记录到文档中！
设计 → docs/plans/
提案 → openspec/proposals/
```

### 规则 4：工作日志更新 ⭐ **新增**

```
完成任何开发任务后，必须更新项目工作日志！
日志位置 → {项目目录}/docs/WORK-LOG.md

必须记录内容：
✅ 完成的任务和文件
✅ 使用的技术和方法
✅ 遇到的问题和解决方案
✅ 下一步计划
✅ 当前进度总览

格式要求：
- 使用日期标题（## YYYY-MM-DD）
- 清晰的章节划分（✅ 完成 / ❌ 待开发 / 📋 下一步）
- 代码块和列表展示文件结构
- 表格展示进度总览

示例：
## 2026-01-30 下午
### ✅ 完成内容
#### 1. 数据库层实现
- **文件**：`electron/database/db.ts`
- **内容**：SQLite 数据库初始化...

### ❌ 待开发部分
#### 1. 提醒系统（P0）
- **需要实现**：scheduler.ts、timeline.ts...

### 📊 当前进度总览
| 模块 | 状态 | 完成度 |
```

---

## 🔗 相关文档

- [Superpowers README](tools/superpowers/README.md)
- [OpenSpec AGENTS.md](tools/OpenSpec-Chinese/AGENTS.md)
- [全局文件组织规范](.global/rules/FILE_ORGANIZATION_RULES.md)

---

## 📝 版本历史

- **2026-01-30** - 添加工作日志更新要求（规则 4）
  - 在核心工作流程中添加第 4 步：更新工作日志
  - 添加规则 4：工作日志更新规范
  - 在工作流程示例中添加更新工作日志步骤
  - 规范工作日志格式和内容要求

- **2026-01-19** - 初始版本，集成 superpowers 和 OpenSpec

---

> 💡 **提示**：这个文件是全局的工作流程规范，所有项目都应该遵循！
