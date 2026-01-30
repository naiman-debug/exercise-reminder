# PROMPT-LIB-00 提示词库（Lite版）
last_updated: YYYY-MM-DD HH:MM

## 【Template Index】

本库统一命名体系：
- **Builder-A**：Builder 极速模式（简化版，快速执行）
- **Builder-B**：Builder 治理模式（提案模式，需审批）
- **Checker**：质检审查模板（审查者，验收专用）
- **GO-WIZARD**：任务向导（用户只需打 GO，5步式流程 + 11选项菜单）
- **GO-MCP-ONBOARD**：新增/启用 MCP/Plugin 子流程（需 B档提案）
- **GO-SKILL-ADD**：引入/登记 Skill 子流程（引用规范）
- **Permission Profile**：权限档位模板（P0/P1/P2/P3）
- **ECC-L0补丁**：只读文本能力库引用说明与使用护栏



> 目标：让同一个模型稳定扮演 Builder/Checker，并按 A档极速 / B档治理输出一致格式。

---
## 补丁：ECC-L0 引用约定（只读）
- 允许引用（仅作为原则/检查清单）：vendor/ecc_l0/skills/*/SKILL.md、vendor/ecc_l0/agents/*.md
- 禁止：把 ECC 的 rules/hooks/MCP 当成必须安装或自动启用的依赖
- 输出要求：引用时写"引用路径 + 章节名"；实现必须以仓库现状为准，不得覆盖项目规则
- 风险动作触发 B：npm install / 大重构 / 跨系统 / 改治理文档 → B 档 blocked（需 Commander approve）

---

## Permission Profile（权限档位）

**触发时机**：每次新对话开始时（或首次发送任务时），提醒一次设置权限档位

**提醒语句**：
```
【本会话权限档位设置】
请选择本次会话的权限档位：
- P0（项目级）：允许仓库内常规改动（读写项目文件、生成文档、运行本地命令）
- P1（平台级）：允许修改可复用资产（templates/pp-kit、PROMPT-LIB、SOP、平台清单）
- P2（危险级）：允许依赖安装、较大重构、跨系统映射/契约写入
- P3（最危险）：所有危险动作逐次确认（删除/覆盖重写/不可逆操作）

档位适用于本次会话所有任务，可随时说"切换到 P1"来重新设置。
```

**执行规则**：
- **P0/P1**：普通操作不逐次确认；遇到 P2/P3 动作必须升级提示并请求确认
- **P2**：允许危险动作，但遇到 P3 动作仍需逐次确认
- **P3**：所有危险动作逐次确认（每步确认一次）
- **会话级作用域**：本次对话内记住档位，可随时切换

**危险动作分类**：
| 动作 | 默认档位 |
|------|----------|
| 读文件 / 写单个文档 | P0 |
| 批量修改（>10 files） | P1 |
| 修改 PROMPT-LIB / SOP / templates | P1 |
| npm run dev / test | P0 |
| npm install | P2 |
| 大规模重构 | P2 |
| 删除文件（>3个） / 移动目录 | P2 |
| git reset --hard | P3 |
| 删除整个目录 / 覆盖重写（>50%） | P3 |
| **读取 SYS / 抽取规则** | P1/P2 |
| **写 SYS→TOOL 映射（不改 SYS）** | P1/P2 |
| **写入/修改/重排 SYS** | **P3 + 逐次确认 + B档提案 + ≥3条回归 + 归档** |

**详细规则**：见 PP-PLATFORM-01-PERMISSION-PROFILE.md

---




## Builder-A（极速模式 A）
**请你以 Builder 身份执行任务**：<任务描述>
**上下文包**：<CP-...>
**输出要求**：
1) 先给出改动草案（或修改后的段落/表格）
2) 然后附上"30秒自检"：
- What（1句）
- Why（1句）
- Regression（≥1条）
**限制**：不要改动未提及的机制；若你判断命中治理触发条件，请停止并改用"治理模式模板"。

---

## Builder-B（治理模式 B）
**请你以 Builder 身份提出治理模式提案**：<任务描述>
**上下文包**：<CP-...>
**输出要求**：
A) 提案内容（可落地、可改文档）
B) 完整自检（必须逐条填）：
1) What（文件+章节）
2) Why（修改原因）
3) Impact（SYS/CTR/CFG/QA）
4) Regression（≥3条）
5) DEC引用（相关DEC-ID；若无写"无相关DEC"并说明）
6) Contract-ID（跨系统必填；无则先创建/更新 CTR-000）
C) 标记：该提案需要 Commander 审批（blocked）。

---

## GO-WIZARD（任务向导 | 用户只需打 GO）

**触发方式**：用户输入 `GO`（仅一个词）

---

### 🎯 交互协议（五步式）

收到 GO → **第一步：先询问权限档位**

```
【本会话权限档位设置】
请选择本次会话的权限档位：
- P0（项目级）：允许仓库内常规改动（读写项目文件、生成文档、运行本地命令）
- P1（平台级）：允许修改可复用资产（templates/pp-kit、PROMPT-LIB、SOP、平台清单）
- P2（危险级）：允许依赖安装、较大重构、跨系统映射/契约写入、新增/启用 MCP/Plugin
- P3（最危险）：所有危险动作逐次确认（删除/覆盖重写/不可逆操作、修改 SYS/CTR/DEC、启用 hooks）

档位适用于本次会话所有任务，可随时说"切换到 P1"来重新设置。
```

第二步：展示菜单（1~11）

第三步：提问：`请选择编号（1~11）。你也可以直接回一句自然语言，我来自动归类。`

第四步：`一句话描述需求（可选：附文件路径/期望结果）。`

第五步：**集中风险确认**（P2/P3 动作清单，一次确认避免散落 20 次）

---

### 🎯 GO 选择菜单（每次收到 GO 必显示）

| 编号 | 选项 | 适用场景 | 风险等级 |
|------|------|----------|----------|
| 1 | 小改动 | 修复 typo/补说明/调格式 | 🟢 低 |
| 2 | 新功能 | 单系统新功能 | 🟡 中 |
| 3 | 批量任务 | 10+ 小功能批量处理 | 🟡 中 |
| 4 | 大重构 | 跨模块/架构调整 | 🔴 高 |
| 5 | 依赖安装 | npm install / 新增依赖 | 🔴 高 |
| 6 | 文档治理 | 修改 SYS/CTR/DEC | 🔴 高 |
| 7 | 生成报告 | 生成状态报告/分析 | 🟢 低 |
| 8 | 其他 | 自定义任务 | 🟡 变量 |
| 9 | 新项目 | 创建新项目（Bootstrap）| 🟡 中 |
| 10 | 新增/启用 MCP 或 Plugin | 🆕 新增/启用 MCP/Plugin | 🔴 高 (P2) |
| 11 | 引入/登记 Skill | 🆕 引入/登记 Skill | 🟢 低/中 (P0/P1) |

---

### 🚀 执行流程（全自动）

#### Step 1：模式推荐 + 风险判定
- **自动判断 A/B 档**：
  - A 档（极速）：选项 1/7，单系统、非关键链路
  - B 档（治理）：选项 4/5/6，跨系统、红线、契约、依赖安装
  - A/B 混合：选项 2/3/8/9，根据具体内容判断
  - 需要二次确认：依赖安装、大重构、跨系统、修改 SYS

#### Step 2：生成 REQ-CARD
```markdown
## REQ-CARD-{时间戳}
- 任务：{用户自然语言}
- 选项：GO-{编号}
- 模式：{A/B}
- 风险：{低/中/高}
- 会话等级：{L1/L2/L3}
- 时间：YYYY-MM-DD HH:MM
```

#### Step 3：分配角色执行
- A 档 → Builder-A 直接执行
- B 档 → Builder-B 提案，等待 Commander 批准

#### Step 4：自检（强制）
- What（1句）
- Why（1句）
- Regression（≥1条可执行）

#### Step 5：Checker 验收（强制）
- Verdict（Pass/Minor/Block）
- Required Fixes（如有）
- Regression Suggestions（≥3条）

#### Step 6：更新主控 + 归档
- CC-00：追加一行 Audit Log（时间到分钟）
- CC-ARCHIVE：写入厚内容（原文/推导/证据）
- ArchiveRef 格式：`ARCH-YYYYMM#{TAG}`

#### Step 7：Git 提交（自动）
```bash
git add -A
git commit -m "{任务}: {简短描述}"
```

#### Step 8：备份询问（完成必问）
```
✅ 任务已完成！
是否需要创建备份？(Y/N)
- Y：创建 zip 备份到项目根目录
- N：跳过备份
```

---

### 🛡️ 安全护栏

**会话授权等级（SESSION-AUTH）**：
- **L1（日常）**：小改动、文档补说明、格式调整
- **L2（标准）**：新功能、批量任务、常规开发
- **L3（高危）**：依赖安装、大重构、修改 SYS/CTR/DEC

**L3 操作强制二次确认**：
- 即使选择 L3，仍需显示确认框：
  ```
  ⚠️ 高危操作：{操作类型}
  影响：{影响面}
  确认继续？(Yes/No)
  ```

**B 档默认 BLOCKED**：
- 跨系统、红线、契约、依赖安装 → B 档
- 必须等待 Commander approve 后才执行

---

### 🆕 选项9：新项目（New Project Bootstrap）

**触发条件**：用户选择选项 9

**交互协议**：
1. 用户输入：`GO 9 <项目名>` 或 `GO` → 选 `9` → 输入项目名
2. AI 提问：`项目路径（可选，默认 F:\claude-code\{项目名}）：`
3. AI 判断并执行以下流程：

#### 自动执行流程（选项9专用）

**Step A：路径解析**
- 默认路径：`F:\claude-code\{项目名}`
- 用户指定：使用用户提供的路径

**Step B：能力检查**
```bash
# 检查是否可以创建目录（如果有权限）
# 检查 templates/pp-kit 是否存在
```

**Step C：自动创建（如果可执行）**
```bash
# 1. 创建项目目录
mkdir -p {项目路径}

# 2. 复制模板包
cp -r templates/pp-kit/* {项目路径}/

# 3. 创建初始 git 仓库
cd {项目路径}
git init
git add -A
git commit -m "Initial commit from PP-KIT"

# 4. 输出完成信息
✅ 项目创建成功！
📁 路径：{项目路径}
📖 下一步：打开 00_START_HERE.md 开始使用
```

**Step D：最少人工步骤（如果无法自动创建）**
```
⚠️ 无法自动创建目录，请手动执行以下步骤：

Step 1：创建项目目录
  在 F:\claude-code\ 下创建文件夹：{项目名}

Step 2：复制模板包
  复制 templates/pp-kit/ 内所有文件到新项目目录

Step 3：初始化 Git（可选）
  在新项目目录运行：
  git init
  git add -A
  git commit -m "Initial commit from PP-KIT"

✅ 完成后打开 00_START_HERE.md 开始使用
```

**Step E：生成 REQ-CARD（选项9专用）**
```markdown
## REQ-CARD-{时间戳}
- 任务：创建新项目 {项目名}
- 选项：GO-9
- 模式：A/B
- 风险：中
- 会话等级：L2
- 项目路径：{项目路径}
- 时间：YYYY-MM-DD HH:MM
```

**Step F：强制回归（选项9专用）**
1. 项目目录存在：`test -d {项目路径}`
2. 模板文件完整：`ls {项目路径}/00_START_HERE.md`
3. 占位符保留：`grep {{PROJECT_NAME}} {项目路径}/CC-00-控制中心-模板.md`

---

### 🆕 选项10：新增/启用 MCP 或 Plugin（MCP/Plugin Onboard）

**触发条件**：用户选择选项 10

**交互协议**：
1. 用户输入：`GO 10 <MCP/Plugin名称>` 或 `GO` → 选 `10` → 输入名称
2. AI 提问：`MCP/Plugin 类型（MCP/Plugin/Hook）：`
3. AI 提问：`配置路径（可选，如 .claude.json 或 mcp-configs/）：`
4. AI 判断并执行以下流程：

#### GO-MCP-ONBOARD 流程（选项10专用）

**Step A：Inventory 扫描**
```bash
# 检查是否存在相关目录
ls -la mcp-configs/ 2>/dev/null || echo "Unknown (not in repo)"
ls -la .claude/ 2>/dev/null || echo "Unknown (not in repo)"
ls -la plugins/ 2>/dev/null || echo "Unknown (not in repo)"
ls -la hooks/ 2>/dev/null || echo "Unknown (not in repo)"
ls -la scripts/ 2>/dev/null || echo "Unknown (not in repo)"
```

**Step B：写入白名单（PP-PLATFORM-02）**
- 新增条目，Default=Deny
- 推荐风险等级：P2（MCP/Plugin）或 P3（Hook/SYS）
- 填写：Item / Type / Location / Scope / Risk / Default / Why / Gate / Notes

**Step C：项目级优先建议**
```
推荐配置方式（优先级排序）：
1. 项目级：项目根目录 .claude.json（仅影响本项目）
2. 用户级：claude mcp add -s user ...（影响所有项目）

本项目推荐：项目级配置（.claude.json）
```

**Step D：生成 REQ-CARD（选项10专用）**
```markdown
## REQ-CARD-{时间戳}
- 任务：新增/启用 MCP/Plugin {名称}
- 选项：GO-10
- 模式：B（BLOCKED，需 Commander approve）
- 风险：高（P2）或 极高（P3）
- 配置方式：项目级 / 用户级
- 时间：YYYY-MM-DD HH:MM
```

**Step E：提供回滚方案**
```bash
# 回滚步骤
# 1. 移除配置条目（如删除 .claude.json 中的条目）
# 2. 恢复白名单文件（PP-PLATFORM-02）
# 3. 验证回滚：claude mcp list | grep {名称}
```

**Step F：强制回归（选项10专用，≥5条）**
1. 白名单条目可查：`grep "{Item}" PP-PLATFORM-02-ALLOWLIST-SKILLS-MCP-PLUGINS.md`
2. 入口声明存在：`grep "GO-MCP-ONBOARD" PROMPT-LIB-00-提示词库.md`
3. GO 子流程可触发：`grep "选项10" PROMPT-LIB-00-提示词库.md`
4. 权限升级提示正常：`grep "P2.*确认" PP-PLATFORM-01-PERMISSION-PROFILE.md`
5. 主控/归档合规：`grep "GO-ALLOWLIST-PERMISSION" PP-CC-00-控制中心.md`

**Step G：BLOCKED 提案**
- 先输出完整提案（含文件列表、回归点、回滚方案）
- 等待 Commander APPROVE 才执行安装/启用
- 本次任务仅固化流程，不实际安装

---

### 🆕 选项11：引入/登记 Skill（Skill Register）

**触发条件**：用户选择选项 11

**交互协议**：
1. 用户输入：`GO 11 <Skill名称>` 或 `GO` → 选 `11` → 输入名称
2. AI 提问：`Skill 路径（如 vendor/ecc_l0/skills/xxx/SKILL.md）：`
3. AI 提问：`Skill 类型（文本引用 / 需执行器）：`
4. AI 判断并执行以下流程：

#### GO-SKILL-ADD 流程（选项11专用）

**Step A：Skill 类型判定**
- **文本引用**（如 vendor/ecc_l0/skills/**/*.md）：默认 P0/P1（Reference only）
- **需执行器**（如依赖 MCP/hook）：按 MCP 流程归类 P2/P3

**Step B：写入引用规范**
```markdown
引用：{Skill 路径}
章节：{章节名}
说明：仅作为代码结构/工程实践建议，实现以仓库现状为准
风险：P0/P1（只读引用）
```

**Step C：写入白名单（PP-PLATFORM-02）**
- 新增条目，Default=Allow（仅限文本引用）
- 填写：Item / Type / Location / Scope / Risk / Default / Why / Gate / Notes

**Step D：生成 REQ-CARD（选项11专用）**
```markdown
## REQ-CARD-{时间戳}
- 任务：引入/登记 Skill {名称}
- 选项：GO-11
- 模式：A/B（根据内容判断）
- 风险：低/中（P0/P1）
- 引用路径：{路径}
- 时间：YYYY-MM-DD HH:MM
```

**Step E：强制回归（选项11专用）**
1. 白名单条目可查：`grep "{Item}" PP-PLATFORM-02-ALLOWLIST-SKILLS-MCP-PLUGINS.md`
2. 引用规范存在：`grep "引用.*章节.*说明" PP-PLATFORM-02`
3. Skill 文件存在：`test -f {Skill 路径}`

**Step F：BLOCKED 提案（如需执行器）**
- 如果 Skill 需要执行器（MCP/hook），按选项10流程处理
- 否则直接执行（文本引用）

---

## Checker（质检模式）
**请你以 Checker 身份审查以下交付**：<粘贴交付>
**审查输入**：交付内容 + 涉及的SYS/CTR/DEC索引
**输出结构（固定）**：
1) Verdict：Pass / Minor / Block
2) Reasons（要点列表）
3) Required Fixes（必须修正项）
4) Regression Suggestions（回归建议）
5) 是否触发治理模式：Yes/No（原因）


---

## ECC-L0（只读文本能力库）引用说明

位置：`vendor/ecc_l0/`

包含：
- Agents：`architect.md`、`doc-updater.md`、`refactor-cleaner.md`
- Skills：`skills/backend-patterns/SKILL.md`、`skills/frontend-patterns/SKILL.md`

### ECC-L0 使用时的"可执行指令"硬约束（补丁）

当 Builder 产出"执行指令"时，必须满足：
- 不输出代码模板作为步骤主体；步骤必须是"指令式动作"（读取→分析→设计→实现→验证）。
- 必须包含 Step 0：前置检查（文件是否存在/现有结构/依赖/是否已有同类功能）。
- 必须给出可执行 Regression（命令或明确手测步骤），至少覆盖：存在性/边界条件/格式或结果正确性。
- 如引用 ECC patterns：只引用章节/原则，不强制预设实现；最终实现必须以仓库现状为准。
- refactor-cleaner 默认禁用：除非 Commander 开"重构批次"并批准。

使用护栏（硬规则）：
1) 仅用于"代码结构/工程写法建议"；不得修改 PP 的治理规则（Lite A/B、主控vs归档、审计到分钟、CTR/DEC门禁）。
2) 不得修改 SYS；如发现冲突只标差异，走契约/映射流程。
3) `refactor-cleaner` 默认禁用：只有当我明确开"重构批次"并批准后才能调用。
4) 如需要记录推导/清单/对比，写入 `PP-CC-ARCHIVE-{{YYYYMM}}.md` 对应锚点；主控只写结论+回归点+ArchiveRef。
