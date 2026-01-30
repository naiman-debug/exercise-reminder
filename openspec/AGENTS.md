# OpenSpec 项目配置

> **项目**：全局配置
> **用途**：定义项目的 OpenSpec 规范流程

---

## OpenSpec 触发条件

当满足以下任一条件时，必须使用 OpenSpec：

1. **规划或提案相关**
   - 提到：proposal, spec, change, plan
   - 需要创建技术提案
   - 需要编写规范文档

2. **重要变更**
   - 新功能（非小修复）
   - 破坏性变更
   - 架构调整
   - 重大性能优化
   - 安全相关改动

3. **需求模糊**
   - 需求不明确
   - 需要权威规范才能编码
   - 涉及多个团队协调

---

## OpenSpec 使用流程

### 第一步：检查触发条件

```
当前请求是否满足触发条件？
├─ 是 → 继续下一步
└─ 否 → 跳过 OpenSpec
```

### 第二步：打开 OpenSpec 规范

```markdown
打开文件：F:\claude-code\tools\OpenSpec-Chinese\AGENTS.md
```

### 第三步：创建提案

按照 OpenSpec 规范创建变更提案：

1. **提案格式**
   - 使用 OpenSpec 定义的格式
   - 包含所有必需章节
   - 遵循项目约定

2. **提案内容**
   - 背景和动机
   - 详细描述
   - 实现方案
   - 影响分析
   - 测试计划

3. **提交提案**
   - 保存到 `openspec/proposals/` 目录
   - 等待审批

### 第四步：等待审批

- 提案需要审批才能实施
- 审批通过后可以继续开发
- 审批不通过需要修改提案

---

## 提案目录结构

```
openspec/
├── AGENTS.md                      # 本文件
└── proposals/                     # 提案目录
    ├── YYYY-MM-DD-<title>.md      # 提案文档
    └── ...
```

---

## 快速决策树

```
收到请求
    │
    ├─ 是否涉及规划/提案？
    │   ├─ 是 → 使用 OpenSpec ✓
    │   └─ 否 ↓
    │
    ├─ 是否是重要变更？
    │   ├─ 是 → 使用 OpenSpec ✓
    │   └─ 否 ↓
    │
    ├─ 需求是否模糊？
    │   ├─ 是 → 使用 OpenSpec ✓
    │   └─ 否 ↓
    │
    └─ 跳过 OpenSpec，直接开发
```

---

## 示例

### 需要 OpenSpec 的请求

✅ "添加一个新的支付模块"
✅ "重构数据库架构"
✅ "实现用户权限系统"
✅ "优化 API 性能（预期提升50%）"

### 不需要 OpenSpec 的请求

❌ "修复登录页面的样式问题"
❌ "更新文档中的错别字"
❌ "添加一个新的按钮"

---

## 与 Superpowers 的集成

OpenSpec 和 Superpowers 是互补的：

```
superpowers
    │
    ├─ brainstorming → 设计阶段
    │                  │
    │                  ├─ 检查：需要 OpenSpec？
    │                  │   ├─ 是 → OpenSpec 提案 → 审批
    │                  │   └─ 否 → 继续
    │                  │
    ├─ writing-plans → 计划阶段
    │
    └─ executing-plans → 执行阶段
```

---

## 参考文档

- [OpenSpec 全局规范](../tools/OpenSpec-Chinese/AGENTS.md)
- [Superpowers 工作流程](../AGENTS.md)
- [全局文件组织规范](../.global/rules/FILE_ORGANIZATION_RULES.md)

---

> 💡 **提示**：OpenSpec 用于重要变更的规范管理，小改动可以直接使用 superpowers 流程。
