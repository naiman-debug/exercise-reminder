# exercise-reminder-v2 Evidence 规范

**项目级 Evidence 化规范 v3.0**

---

## 🚨 Hook 强制检查（提交前自动执行）

### 为什么要 Hook？

**问题**：只写文档不强制执行，AI 会偷懒用假验证。

**解决**：Git commit 时自动检查 REGRESSION 是否真实运行。

---

### Hook-L2：REGRESSION 真实性检查

**触发时机**：`git commit` 命令执行时

**检查逻辑**：

1. 读取最新的 `CC-ARCHIVE-YYYYMMDD.md` 文件
2. 查找最新的任务记录
3. 检查该任务的 REGRESSION 内容

**假验证模式（自动拦截）**：

| 模式 | 示例 | 拦截 |
|------|------|------|
| 只检查导入 | `python -c "from src.ui.dialogs import"` | ❌ 拦截 |
| 只检查文件 | `ls src/main.py` | ❌ 拦截 |
| 只检查内容 | `grep "pattern" file` | ❌ 拦截 |
| 只检查存在 | `cat docs/EVIDENCE-SPEC.md` | ❌ 拦截 |

**真实运行模式（允许通过）**：

| 模式 | 示例 | 说明 |
|------|------|------|
| 启动应用 | `python src/main.py` | ✅ 允许 |
| 打开演示 | `python demo.py` | ✅ 允许 |
| 运行测试 | `python tests/test_xxx.py` | ✅ 允许 |
| 验证输出 | 命令 → 预期结果 | ✅ 允许 |

**拦截行为**：
```
❌ Hook 检查失败：检测到假验证模式

检测到的假验证：
  - python -c "from src.ui.dialogs import"

请修改 CC-ARCHIVE 文件中的 REGRESSION，使用实际运行的命令。
正确的 REGRESSION 示例：
  python src/main.py → 应用启动成功

Commit 被拦截，请修复后重试。
```

**绕过方式**（紧急情况）：
```bash
git commit --no-verify -m "message"
```
⚠️ 警告：使用 `--no-verify` 跳过 Hook 会留下记录。

---

## 📋 角色定义

### Builder（构建者）

**职责**：
- 编写代码
- 修复 bug
- 实现功能

**交付**：
- 可运行的代码

---

### Tester（测试用例设计师）🆕

**职责**：
- 设计测试用例
- 编写测试脚本
- 定义验证标准

**交付**：
- 测试用例文档
- 自动化测试脚本
- 验证标准

**工作流程**：
1. Builder 完成代码
2. Tester 设计测试用例
3. Tester 运行测试验证
4. 验证通过后交付

---

### Checker（质检者）

**职责**：
- 验证 Evidence 完整性
- 检查 REGRESSION 真实性
- 给出 CHECKER_VERDICT

**交付**：
- 验证报告
- PASS/MINOR/BLOCK 判定

---

## Evidence 字段定义

| 字段 | 格式 | 必须 | 位置 |
|------|------|------|------|
| **GO_SESSION** | `GO-YYYYMMDD-HHMM-{4位随机}` | ✅ | 00_START_HERE + CC-ARCHIVE |
| **PERMISSION** | `P0` \| `P1` \| `P2` \| `P3` | ✅ | 任务描述 |
| **REGRESSION** | ≥3 条**实际运行**命令 | ✅ | 完成后的验证区 |
| **TEST_CASES** | 测试用例文档链接 | ✅ | 新增 |
| **CHECKER_VERDICT** | `PASS` \| `MINOR` \| `BLOCK` | ✅ | 最终结论 |
| **ARCHIVE_REF** | `CC-ARCHIVE-YYYYMMDD#TAG` | ✅ | 主控引用 |

---

## GO_SESSION 生成

```python
import datetime
import random
import string

def generate_go_session():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M")
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"GO-{timestamp}-{rand}"
```

---

## 任务执行流程

```
Builder 写代码
    ↓
Tester 设计测试用例 + 运行测试
    ↓
Checker 验证 Evidence + 给出 VERDICT
    ↓
git commit（Hook 自动检查 REGRESSION）
    ↓
更新归档 + 00_START_HERE
```

---

## 任务执行模板

### 开始任务时

```
【任务开始】
GO_SESSION: GO-20260126-0130-A7F2
PERMISSION: P0
任务: {简短描述}
```

### 完成任务时（必须包含）

```
【任务完成】
GO_SESSION: GO-20260126-0130-A7F2
CHECKER_VERDICT: PASS

REGRESSION（必须实际运行，会被 Hook 检查）:
1. {实际运行的命令} → {预期结果}
2. {实际运行的命令} → {预期结果}
3. {实际运行的命令} → {预期结果}

TEST_CASES: {测试用例文档路径}

ARCHIVE_REF: CC-ARCHIVE-20260126#TASK-{名称}
```

---

## REGRESSION 规范（重点）

### ✅ 正确的 REGRESSION

必须实际运行代码，验证功能正常：

```
1. python src/main.py → 应用启动，托盘图标显示，无报错
2. python demo.py → 演示菜单打开，所有按钮可点击
3. python -c "from src.models.database import get_db_manager; db = get_db_manager(); db.initialize_database(); print('OK')" → 数据库初始化成功
```

### ❌ 错误的 REGRESSION（会被 Hook 拦截）

只检查静态内容，不验证运行：

```
1. ls src/main.py → 文件存在（不验证能否运行）
2. python -c "from src.ui.dialogs import StandReminderDialog" → 导入成功（不验证能否显示）
3. grep "def test" tests/ → 函数存在（不验证能否通过）
```

### 判断标准

**问题**：如何判断是真实验证还是假验证？

**测试**：运行命令后，是否产生了**实际的行为**？
- 如果只检查"文件存在/导入成功" → 假验证
- 如果启动了应用/显示了界面/执行了逻辑 → 真实验证

---

## TEST_CASES 测试用例设计

### 测试用例模板

每个任务应该有对应的测试用例文档：

```markdown
# TEST-{任务名称}

## 测试环境
- 操作系统：Windows 11
- Python 版本：3.11
- 依赖：PySide6, peewee

## 测试用例

### TC-001: 强制站立弹窗显示
- **步骤**：运行 `python demo.py` → 点击"强制站立提醒"
- **预期**：弹窗打开，显示倒计时
- **优先级**：P0

### TC-002: 微运动弹窗显示
- **步骤**：运行 `python demo.py` → 点击"微运动提醒"
- **预期**：弹窗打开，显示动作信息
- **优先级**：P0
```

---

## 写入位置

- **00_START_HERE.md**：【当前快照】区域更新
- **CC-ARCHIVE-YYYYMMDD.md**（如不存在则创建）：完整任务记录
- **docs/TEST-{任务名称}.md**（如需要）：测试用例文档

---

## 验证脚本

参见 `scripts/validate_evidence.py`（静态检查）和 `.git/hooks/pre-commit`（Hook 检查）

---

## 示例

### 任务：修复弹窗 bug

**角色分工**：
- **Builder**：修复代码
- **Tester**：设计测试用例
- **Checker**：验证 Evidence

**Builder 完成**：
```
【任务完成】
GO_SESSION: GO-20260126-0130-A7F2

REGRESSION:
1. python demo.py → 点击"强制站立提醒"按钮，弹窗正常显示
2. python demo.py → 点击"依次演示所有弹窗"，3个弹窗依次显示
3. python src/main.py → 应用启动，托盘图标显示，无报错

TEST_CASES: docs/TEST-FIX-DIALOG.md

ARCHIVE_REF: CC-ARCHIVE-20260126#FIX-DIALOG-BUG
```

**Tester 设计测试用例**：创建 `docs/TEST-FIX-DIALOG.md`

**Checker 验证**：
1. 检查 REGRESSION 是否实际运行 ✅
2. 检查 TEST_CASES 是否存在 ✅
3. 运行实际测试验证 ✅
4. CHECKER_VERDICT: PASS

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-01-26 02:30 | 初始版本（无 Hook，无 Tester） |
| 2.0 | 2026-01-26 02:45 | 升级：强调 REGRESSION 必须实际运行（但仍是文档，无强制） |
| **3.0** | **2026-01-26 03:00** | **重大升级：添加 Hook 强制检查 + Tester 角色** |

---

## v3.0 升级记录

### 问题发现
1. v2.0 虽然强调"必须实际运行"，但只是文档，无强制机制
2. AI 仍用假验证（`python -c "import xxx"`）
3. 实际运行 `python src/main.py` 时发现错误
4. 说明**只有文档不够，需要 Hook 强制执行**

### v3.0 改进
1. **新增**：Hook 强制检查章节（放在文档最前面）
2. **新增**：Tester 测试用例设计师角色
3. **新增**：TEST_CASES 字段
4. **新增**：角色定义和工作流程
5. **新增**：假验证模式拦截规则
6. **调整**：章节顺序，Hook 在任务执行之前

### Hook 实现
- 文件：`.git/hooks/pre-commit`
- 检查假验证模式
- 拦截 git commit 直到修复
- 可用 `--no-verify` 紧急绕过（会记录）

### 经验教训
- 文档只能建议，不能强制
- Hook 是强制执行的唯一方式
- Hook 必须放在文档前面，否则 AI 会跳过不读
- 必须有 Tester 角色设计测试用例
