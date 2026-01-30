# SOP-01 快速启动指南（新项目必读）

版本：v1.0
last_updated: YYYY-MM-DD HH:MM

---

## 🎯 本指南目标

让新项目在 30 分钟内完成：
1) 复制模板并替换占位符
2) 初始化控制中心
3) 完成第一个 P0 任务

---

## Step 1：复制模板（5分钟）

### 1.1 复制文件
```bash
# 方法1：命令行复制
cp -r templates/pp-kit/* {新项目目录}/

# 方法2：手动复制
# 将 templates/pp-kit/ 下所有文件复制到新项目根目录
```

### 1.2 重命名文件
```bash
# CC-ARCHIVE-YYYYMM-模板.md → CC-ARCHIVE-{YYYYMM}.md
# 例如：CC-ARCHIVE-202501-模板.md → CC-ARCHIVE-202501.md
```

---

## Step 2：替换占位符（10分钟）

### 2.1 全局替换
使用编辑器的"查找替换"功能，替换以下占位符：

| 占位符 | 替换为 | 示例 |
|--------|--------|------|
| `{项目名}` | 你的项目名称 | `我的游戏项目` |
| `{你的名字}` | Commander 名称 | `张三` |
| `{项目根目录}` | 实际路径 | `F:\projects\my-game` |
| `YYYY-MM-DD HH:MM` | 当前时间 | `2025-01-25 15:00` |

### 2.2 手动填写必填字段
打开 `00_START_HERE.md`，填写：
- repo_root: 你的项目根目录
- 【当前快照】：项目当前状态（如果已有）
- 【今日边界】：已完成/未完成事项
- 【明日唯一 P0】：第一个任务

---

## Step 3：初始化控制中心（10分钟）

### 3.1 填写 CC-00 关键字段
打开 `CC-00-控制中心.md`，填写：

| 字段 | 填写内容 |
|------|----------|
| last_updated | 当前时间 |
| commander | 你的名字 |
| mode_default | A（极速）或 B（治理） |
| 今日健康度 | 根据实际情况填写 |
| Action Queue | 第一个 P0 任务 |

### 3.2 创建第一个任务
在 Action Queue 中添加：

```markdown
| P0 | INIT-001 | A | 初始化项目模板 | 复制并替换模板文件 | 00_START_HERE已更新 + CC-00已填写 | 🟢 active | Builder | No |
```

---

## Step 4：验证配置（5分钟）

### 4.1 检查文件完整性
确认以下文件存在且重命名正确：
- ✅ 00_START_HERE.md
- ✅ CC-00-控制中心.md
- ✅ CC-ARCHIVE-{YYYYMM}.md
- ✅ PROMPT-LIB-00-提示词库.md
- ✅ README.md
- ✅ SOP-01-快速启动.md

### 4.2 测试工作流
1) 打开 00_START_HERE.md，阅读 CHAT HANDOFF BLOCK
2) 打开 CC-00-控制中心.md，查看 Action Queue
3) 发送 `DAILY SNAPSHOT` 命令给 AI，测试是否正常工作

---

## Step 5：开始第一天工作（🎉）

### 5.1 发送第一个任务
```text
你是 Builder（A档）。任务：{你的第一个P0任务}
上下文：00_START_HERE.md + CC-00-控制中心.md
输出要求：
1) 给出执行草案
2) 附上自检（What/Why/Regression≥1）
```

### 5.2 验收标准
- ✅ 00_STARTHERE 已更新快照
- ✅ CC-00 已有第一条 Audit Log
- ✅ 第一个 P0 任务已完成

---

## 📋 检查清单

使用以下清单确认启动完成：

- [ ] 所有模板文件已复制到项目根目录
- [ ] CC-ARCHIVE 已重命名（包含当前年月）
- [ ] 所有占位符已替换
- [ ] 00_START_HERE 已填写当前快照
- [ ] CC-00 已填写第一个 P0 任务
- [ ] 已发送 `DAILY SNAPSHOT` 测试工作流
- [ ] 第一个任务已分配给 AI

---

## 🆘 遇到问题？

### 问题：找不到某个文件
检查：templates/pp-kit/ 目录是否存在，文件是否完整复制

### 问题：AI 不理解模板
检查：00_START_HERE 的 CHAT HANDOFF BLOCK 是否正确复制

### 问题：CC-00 格式错乱
检查：是否使用支持 Markdown 的编辑器（VSCode / Typora）

---

## 📚 下一步

启动完成后，建议阅读：
- PP-SOP-00-Commander操作手册.md（详细操作手册）
- PROMPT-LIB-00-提示词库.md（Builder/Checker 模板）
