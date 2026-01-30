# Claude Code 全局配置

> 📍 工作目录：F:\claude-code\

---

## 📋 全局规则

### ⚠️ 文件组织规范（必读）

**适用范围**：所有项目

**核心原则**：
- 🚫 禁止随意在项目根目录创建文件
- 📂 所有文件必须有明确的归属目录
- 📦 不确定归属时使用临时目录 `temp/inbox/`

**详细文档**：[.global/rules/FILE_ORGANIZATION_RULES.md](.global/rules/FILE_ORGANIZATION_RULES.md)

**快速决策**：
```
要创建文件？
  ├─ 知道放哪里 → 放入对应目录
  └─ 不确定 → temp/inbox/ (之后再整理)
```

---

## 📂 目录结构

```
F:\claude-code\
├── .global/              # 全局规则
│   ├── README.md         # 规则索引
│   └── rules/            # 具体规则
│
├── docs/                 # 🌐 全局文档中心
│   ├── README.md         # 文档索引
│   ├── infra/            # 基础设施文档（MCP/Skill/Agent）
│   ├── plugin/           # Plugin 使用指南
│   └── mcp/              # MCP 服务器文档（旧）
│
├── tools/                # 🛠️ 开发工具
│   ├── superpowers/      # Superpowers 框架
│   └── OpenSpec-Chinese/  # OpenSpec 工具
│
├── openspec/             # 📐 OpenSpec 项目配置
│   └── AGENTS.md         # 项目级配置
│
├── AGENTS.md             # 🤖 AI Agent 工作流程规范
├── claude.md             # 本文件 - 全局配置
│
└── {项目目录}/           # 各个项目
    └── ...              # 其他项目
```

---

## 📝 项目配置模板

每个项目应该有自己的配置：

1. **项目级配置**：`{项目}/CLAUDE.md`
2. **项目说明**：`{项目}/README.md`
3. **当前任务**：`{项目}/CURRENT_TASK.md`

---

## 🤖 AI Agent 工作流程

### 核心流程

所有开发任务必须遵循 [AGENTS.md](AGENTS.md) 中定义的工作流程：

```
1. 技能检查 → 调用相关技能
2. superpowers 流程 → brainstorming → planning → executing
3. OpenSpec 检查 → 重要变更需要规范提案
4. 完成任务
```

### Superpowers

**用途**：完整的软件开发工作流程框架

**主要技能**：
- `brainstorming` - 头脑风暴，细化需求
- `writing-plans` - 编写实现计划
- `executing-plans` - 执行计划
- `test-driven-development` - TDD 测试驱动

**位置**：`F:\claude-code\tools\superpowers\skills\`

### choose-tool (工具选择)

**用途**：自动分析任务并推荐合适的开发工具

**功能**：
- 分析任务类型和复杂度
- 推荐最合适的工具
- 提供快速决策支持

**位置**：`F:\claude-code\.global\skills\choose-tool\`

**详细指南**：[工具选择指南](docs/TOOL_SELECTION_GUIDE.md)

### OpenSpec

**用途**：规范管理和提案流程

**触发条件**：
- 规划或提案
- 新功能、破坏性变更、架构调整
- 重要性能或安全工作
- 需求模糊需要权威规范

**位置**：
- 规范：`F:\claude-code\tools\OpenSpec-Chinese\AGENTS.md`
- 配置：`F:\claude-code\openspec\AGENTS.md`

---

## 🔗 相关链接

### 规则与文档
- [全局规则索引](.global/README.md)
- [文件组织规范](.global/rules/FILE_ORGANIZATION_RULES.md)
- [全局文档中心](docs/README.md)
- [文档更新指南](.global/UPDATE_GUIDE.md)

### 基础设施
- [INFRA.md](INFRA.md) - MCP/Skill/Agent 管理总入口

### 工作流程
- [AGENTS.md](AGENTS.md) - AI Agent 工作流程规范
- [工具选择指南](docs/TOOL_SELECTION_GUIDE.md) - 快速选择合适的工具
- [OpenSpec 配置](openspec/AGENTS.md) - OpenSpec 项目配置
- [Superpowers README](tools/superpowers/README.md)
- [OpenSpec AGENTS](tools/OpenSpec-Chinese/AGENTS.md)
