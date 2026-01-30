# vendor/ 目录说明（可选）

## 📦 这个目录是什么？

`vendor/` 目录用于存放"项目内隔离"的第三方资源/能力库。

默认情况下，本目录为空。如需引入外部能力库（如 ECC-L0），请按以下规则操作。

---

## 🎯 使用规则（硬约束）

### 规则1：隔离原则
- 所有第三方资源必须放在 `vendor/` 子目录下
- 不得修改项目核心文档体系（SYS/CTR/DEC）
- 不得启用 MCP/hooks 或改变 AI 全局行为

### 规则2：可选引用
- 第三方能力库为"可选引用"，非必需
- 如不使用，忽略本目录即可

### 规则3：回滚方案
- 删除 `vendor/` 目录即可完全回滚
- 不影响项目核心文档与治理体系

---

## 📚 ECC-L0 引用说明（可选）

如需使用 ECC-L0（只读文本能力库），请参考以下步骤：

### Step 1：创建目录结构
```bash
mkdir -p vendor/ecc_l0/agents
mkdir -p vendor/ecc_l0/skills
```

### Step 2：放置能力库文件
将 ECC-L0 的 agents 和 skills 文件放入对应目录。

### Step 3：在 PROMPT-LIB 中引用
在 `PROMPT-LIB-00-提示词库.md` 中添加 ECC-L0 引用段落与使用护栏。

---

# ECC-L0（可选）：只读文本能力库

用途：提升 AI 的工程建议质量（前端/后端 patterns、review/checklist），但不改变门禁与项目操作系统。

启用方式（可选）：
- 将 vendor/ecc_l0/ 复制到新项目的 vendor/ecc_l0/
- 在新项目 00_START_HERE 的 HANDOFF BLOCK 中声明 ECC-L0 状态（仅引用，不安装）

硬护栏：
- 不安装 MCP，不启 hooks，不改变 ClaudeCode 全局行为
- ECC-L0 仅用于工程建议，不得修改项目治理规则与文档体系
- 依赖安装/大重构/跨系统/改治理文档 → 必须 B 档 blocked，需 Commander approve



## ⚠️ 重要提醒

1. **默认禁用**：第三方能力库默认禁用，除非明确启用
2. **治理模式**：引入第三方能力库属于 B 档操作，需 Commander 批准
3. **审计到分钟**：任何变更必须写入 CC-00 Audit Log
4. **回归测试**：引入后必须进行回归测试（≥3条）
