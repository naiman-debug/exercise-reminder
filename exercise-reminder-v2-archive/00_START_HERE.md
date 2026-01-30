# 00_START_HERE（强入口：新聊天/新AI/ClaudeCode 必读）
last_updated: 2026-01-26 18:45
repo_root: f:\claude-code\exercise-reminder-v2

---

## ✅ CHAT HANDOFF BLOCK（复制给"聊天窗口AI"的唯一上下文）
你是"资深产品经理 + 执行型工程 + QA门禁"。请按以下规则接管项目，不要问我重复问题。

【事实源】exercise-reminder-v2-SYS-* 为最终设计；其他项目仅作参考，不可反推
【工作方式】单线程推进：只做一个 P0；所有改动必须可回归、可追溯
【记录位置】日常快照写入 00_START_HERE（到分钟）；有交付/决策/验收结论时补写 CC-00（一条结论级记录，含回归点/ArchiveRef）

【项目目标】构建一个简洁高效的 PC 端运动提醒应用，解决久坐问题，定时提醒用户运动

【核心功能】
- 定时提醒：可自定义提醒间隔（如 30 分钟、1 小时）
- 动作指导：展示 20+ 个常见运动动作（开合跳、深蹲、拉伸等）
- 桌面应用：Windows 桌面程序，系统托盘常驻
- 统计追踪：记录每日运动次数和完成情况

【技术方向】
- 桌面应用：Electron / Tauri（推荐）或 Python GUI
- 轻量简洁：专注核心功能，避免过度设计
- 本地存储：无需联网，数据本地保存

【MCP 能力】
- memory：知识图谱记忆（用户偏好、习惯分析）
- sequential-thinking：智能推荐运动动作
- context7：技术文档查询

【设计能力】
- frontend-design skill：生产级前端界面设计（Web/移动端）
  - 用途：UI/UX 设计、组件设计、视觉风格定义
  - 输出：HTML/CSS/JS 代码 + 设计语言指南
  - 转换：Web 设计 → Qt/PySide6 实现
  - 参考：src/ui/design/tokens.py（呼吸感设计系统）
  - 触发：使用 `Skill frontend-design:frontend-design` 调用

【ECC-L0（文本能力库）状态】
- 已引入：vendor/ecc_l0/（仅 agents/skills 文本文档，供参考/引用）
- 禁止：不安装额外 MCP、不启 hooks、不改变 ClaudeCode 全局行为
- 使用边界：ECC-L0 仅用于"代码结构/工程实践建议"，不得修改项目治理规则与文档体系
- 门禁：涉及依赖安装/大重构/跨系统/改治理文档 → 必须 B 档 blocked，等待 Commander approve

【GO-WIZARD（任务向导）触发规则】
- 触发：当用户输入 "GO" 时，必须按 PROMPT-LIB-00 的 GO-WIZARD 模板执行
- 第一步：先询问权限档位（P0/P1/P2/P3），会话级作用域
- 菜单：展示 1~11 选项菜单，让用户选择编号或用自然语言描述
- 流程：权限档位 → 菜单选择 → REQ-CARD → 路径选择 → 集中风险确认 → 执行 → 验收 → 更新主控 → Git 提交
- 集中确认：P2/P3 动作收集成清单，一次确认避免散落 20 次
- 选项9：新项目创建（Bootstrap），自动复制 templates/pp-kit 到新路径
- 选项10：新增/启用 MCP 或 Plugin（需 B档提案）
- 选项11：引入/登记 Skill（引用规范）

【权限档位（Permission Profile）】
- P0 项目级：常规改动（页面、样式、简单功能）
- P1 平台级：修改可复用资产（组件、工具）
- P2 危险级：依赖安装、大重构、MCP 启用
- P3 最危险：逐次确认
- 档位适用于本次会话所有任务，可随时说"切换到 P1"重新设置
- 详见 PP-PLATFORM-01 或 PP-PLATFORM-03 或 PROMPT-LIB Permission Profile 模板

【Allowlist 白名单】
- 统一管理 Skills/MCP/Plugins 的白名单（PP-PLATFORM-02）
- Skills（只读文本引用）：默认 Allow（P0/P1）
- MCP/Plugin（需安装）：默认 Deny（P2），需 GO-10 流程确认
- Unknown 规则：仓库找不到的配置一律写 Unknown（not in repo），禁止脑补
- 详见 PP-PLATFORM-02 Allowlist 白名单

---

## 【当前快照（到分钟）】

2026-01-26 02:45：Evidence 规范升级到 v2.0 + app.py 导入修复
- 回归：python src/main.py → 应用启动成功；python demo.py → 演示菜单可用
- Checker：所有检查通过 [CC-ARCHIVE-20260126#EVIDENCE-SPEC-V2]
- 升级：docs/EVIDENCE-SPEC.md v2.0，强调 REGRESSION 必须实际运行
- 修复：src/core/app.py 添加 Qt 导入
- 教训：假验证（导入成功≠运行成功），必须实际运行测试

## 【今日边界】
- 已完成：PP-KIT 模板复制 + 项目重命名 + 需求沟通启动
- 未完成：PRD 文档、技术选型、UI 设计

## 【明日唯一 P0】
P0：完成项目需求文档（PRD），明确核心功能和用户体验流程

交付物必须包含：
1) exercise-reminder-v2-SYS-01-PRD.md（产品需求文档）
2) 技术选型建议（桌面应用方案：Electron vs Tauri vs Python）
3) 用户流程图（提醒触发 → 动作展示 → 完成记录）

---

## 0) 不可违背的项目操作系统（人/AI通用）
1) **事实源**：exercise-reminder-v2-SYS-* 系列文档是 Source of Truth（冲突以 SYS 为准）。
2) **可回归**：任何交付必须给"Regression 回归点"（可执行验证步骤）。
3) **可追溯**：任何改动必须写入 `CC-00-控制中心.md`（到分钟）。
4) **单线程**：任何时候只推进一个 P0；其余进入 P1/Backlog。
5) **跨系统先契约**：涉及 SYS 间接口/资源/流程联动，先写/改 `CTR-*`，再改 SYS 或代码。

---

## 1) DAILY ROUTINE（每天一次，2分钟）
触发：每天开工 / 或开新聊天前（两者选其一即可）。

### Step A（ClaudeCode / 任意AI）
把下面 Prompt 发给 AI：

```text
你是 Librarian。请基于 CC-00-控制中心.md（最近24小时）生成"DAILY SNAPSHOT"，必须包含三段：
【当前快照（到分钟）】【今日边界】【明日唯一P0】。
要求：20行以内、短句、可直接复制粘贴、不解释不提问。
```

### Step B（你操作）
1) 把 AI 输出复制粘贴到本文件【CHAT HANDOFF BLOCK】的对应段落
2) 更新 last_updated 到当前分钟
3) （可选）用 `git commit -am "snapshot: update 00_START_HERE"` 保存快照

---

## 2) 文档导航（2分钟了解全局）

| 文档类型 | 文件名 | 作用 | 何时读 |
|---------|--------|------|--------|
| 强入口 | 00_START_HERE.md | 当前快照 + 每日例程 | 每天开工/新聊天必读 |
| 控制中心 | CC-00-控制中心.md | P0队列 + 健康度 + 决策点 | 看全局/找任务 |
| 归档 | CC-ARCHIVE-202601.md | 厚内容存放（Checker原文/长推演） | 查细节/查证据 |
| 提示词库 | PROMPT-LIB-00-提示词库.md | Builder/Checker 模板 | 让 AI 执行任务 |
| 主设计索引 | MDI-00-主设计索引.md | 项目快照内存 | 了解全局架构 |
| 契约索引 | CTR-000-契约模板与索引.md | 跨系统交互定义 | 跨系统任务前必读 |
| 决策索引 | DEC-INDEX-00-决策索引.md | 红线/不变量/重大机制 | 治理模式必查 |

---

## 3) 快速命令参考

| 命令 | 作用 | 何时用 |
|------|------|--------|
| `DAILY SNAPSHOT` | 生成今日快照 | 每天开工 |
| `Builder-A` | 极速模式执行 | 小改动/A档任务 |
| `Builder-B` | 治理模式提案 | B档/跨系统/红线 |
| `Checker` | 质检审查 | 验收交付 |
| `git status` | 查看变更状态 | 提交前/收口时 |
| `git log --oneline -10` | 查看最近提交 | 复盘/追溯 |

---

## 4) 应急手册（遇到问题时）

### 问题：AI 跑偏/不听话
- 解决：重新发送 CHAT HANDOFF BLOCK 内容
- 根因：可能是新聊天/上下文丢失

### 问题：不知道当前该做什么
- 解决：读 CC-00 的 Action Queue（P0/P1 ONLY）
- 根因：缺少明确优先级

### 问题：改动后发现有问题
- 解决：`git diff` 查看变更，`git checkout -- file` 回滚单个文件
- 根因：缺少回归点

### 问题：文档太多找不到
- 解决：从 00_START_HERE 开始，按"文档导航"表格跳转
- 根因：缺少入口导航

---

## 5) 技术栈建议（待确认）

### 桌面应用方案

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **Tauri** | 轻量、安全、Rust + Web | 相对较新 | ⭐⭐⭐⭐⭐ |
| **Electron** | 成熟、生态丰富 | 体积大、资源占用高 | ⭐⭐⭐⭐ |
| **Python GUI** | 简单、无需打包 | UI 一般、分发麻烦 | ⭐⭐⭐ |

### 前端技术（如用 Electron/Tauri）
- **框架**：Vue 3（Composition API）
- **UI 组件**：Element Plus / Naive UI
- **状态管理**：Pinia
- **构建工具**：Vite

### 数据存储
- **本地存储**：SQLite / IndexedDB
- **配置文件**：JSON / YAML

---

**维护说明**：
- 本文档由 Commander 维护
- 每天开工时更新【当前快照】
- 有交付时更新 CC-00 控制中心
