# 全局规则和约定

> 🚨 **最高优先级规则**：这些规则适用于所有项目，请务必遵守

---

## 🔥 强制规则：Superpower 工作流程

> **所有开发任务必须使用 superpower 工作流程**

### 📌 规则说明

**核心原则**：
- 🚀 **任何开发任务都必须先检查并调用相关的 superpower 技能**
- 📋 **即使 1% 的可能性适用，也必须调用技能检查**
- ⚡ **技能调用 > 直接编码** - 不跳过技能直接写代码

### 🔄 适用场景

**必须使用 superpower 技能的情况**：
1. ✅ 实现新功能
2. ✅ 修复 bug
3. ✅ 重构代码
4. ✅ 设计新功能
5. ✅ 性能优化
6. ✅ 任何需要编码的任务

### 📁 可用 Superpower 技能

**位置**：`F:\claude-code\tools\superpowers\skills\`

**主要技能**：
- `brainstorming` - 头脑风暴，细化需求
- `writing-plans` - 编写实现计划
- `executing-plans` - 执行计划
- `test-driven-development` - TDD 测试驱动
- `systematic-debugging` - 系统化调试
- `verification-before-completion` - 完成前验证

### 🎯 使用流程

```
1. 用户提出任务
2. 检查是否有适用的 superpower 技能
3. 如果有 → 调用 Skill 工具
4. 按技能指导完成任务
5. 如果无 → 直接处理（但需说明原因）
```

### ⚠️ 违规后果

- 🔴 **代码质量无法保证**
- 🔴 **可能引入新 bug**
- 🔴 **无法系统化解决问题**
- 🔴 **开发效率低下**

### 📖 参考文档

- Superpowers 框架：`tools/superpowers/README.md`
- 使用指南：`.claude/skills/using-superpowers`

---

## 📂 目录结构

```
F:\claude-code\
├── .global/              # 全局规则目录
│   ├── README.md         # 本文件 - 规则索引
│   └── rules/            # 具体规则文档
│       └── FILE_ORGANIZATION_RULES.md
│
├── docs/                 # 🌐 全局文档中心
│   ├── README.md         # 文档索引
│   ├── plugin/           # Plugin 使用指南
│   └── mcp/              # MCP 服务器文档
│
├── claude.md             # 全局 Claude 配置
└── {项目目录}/           # 各个项目
```

---

## 📋 规则列表

### 1️⃣ 文件组织规范

**文档**：`rules/FILE_ORGANIZATION_RULES.md`

**核心原则**：
- 🚫 禁止随意在项目根目录创建文件
- 📂 所有文件必须有明确的归属目录
- 📦 不确定归属时使用临时目录 `temp/inbox/`

**适用范围**：所有项目

**快速决策**：
```
要创建文件？
  ├─ 知道放哪里 → 放入对应目录
  └─ 不确定 → temp/inbox/ (之后再整理)
```

[查看完整规范](rules/FILE_ORGANIZATION_RULES.md)

---

## 🎯 为什么需要全局规则？

### 问题
- 每个项目文件组织方式不一致
- 根目录文件散乱，难以维护
- 新建文件时不知道放哪里

### 解决
- 统一的文件组织规范
- 清晰的目录归属规则
- 临时目录作为缓冲区

---

## 📝 规则使用流程

### 对于新项目

1. 阅读全局规则
2. 按规范创建目录结构
3. 遵循文件组织规范

### 对于现有项目

1. 对照规则检查当前结构
2. 整理散乱的文件
3. 创建 temp/ 临时目录（如果还没有）

### 创建新文件时

1. 先查阅规则文档
2. 确定文件应该放哪里
3. 不确定就放 temp/inbox/

---

## 🔗 相关链接

- [全局文档中心](../docs/README.md) - Plugin、MCP 等通用文档
- [文档更新指南](UPDATE_GUIDE.md) - 如何更新 MCP & Plugin 文档
- **Claude Code 官方文档**：[链接]
- **项目模板**：（待创建）

---

## 🔄 文档更新

当安装新的 MCP 服务器或 Plugin 后：

**快速更新**：
```bash
node .global/scripts/update-mcp-docs.js
```

**详细指南**：[UPDATE_GUIDE.md](UPDATE_GUIDE.md)

---

> 💡 **提示**：这些规则会持续更新，请定期查看最新版本
