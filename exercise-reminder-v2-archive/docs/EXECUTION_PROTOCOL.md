# 执行协议 - 强制设计文档检查

**版本:** v1.0
**优先级:** 最高（超越所有其他规则）

---

## 核心协议

```
在修改 exercise-reminder-v2 项目的任何代码前，必须：

1. 触发 SUPERPOWER 流程
2. 阅读设计文档（DESIGN-UI-001.md）
3. 创建设计-实现对照表
4. 验证实现符合设计
```

---

## 触发机制

### 自动触发（必须实现）

```python
# 在执行任何代码修改前
from src.core.pre_execution_check import pre_execution_check

# 示例1: 修改文件前
def modify_something():
    if not pre_execution_check("修改倒计时闪烁"):
        return  # 阻止执行
    # ... 执行修改

# 示例2: 使用装饰器
@require_design_check
def update_dialog_ui():
    # ... 执行修改
```

### 用户指令触发

以下用户输入必须触发 SUPERPOWER：
- "执行"
- "go"
- "开始"
- "实现"
- "修改"
- "添加"
- "更新"
- "修复"
- "重构"

---

## 设计文档位置

```
docs/DESIGN-UI-001.md  # UI设计规范（主要）
docs/PRD-v2.0.md         # 产品需求文档
```

---

## 检查清单

### 执行前

- [ ] 阅读 DESIGN-UI-001.md 全文
- [ ] 记录关键设计要求到 checklist
- [ ] 确认当前实现与设计的差异
- [ ] 创建修复计划

### 执行后

- [ ] 对照 checklist 逐项验证
- [ ] 运行测试验证
- [ ] 手动测试 UI 效果
- [ ] 确认与设计文档一致

---

## 使用方法

### 方法1: 直接调用

```python
from src.core.pre_execution_check import pre_execution_check

# 开始任何修改前
pre_execution_check("任务描述")

# 然后继续执行
```

### 方法2: 使用 SUPERPOWER 技能

```
用户: "执行：修改倒计时"
    ↓
自动使用 brainstorming 技能
    ↓
brainstorming 会：
  1. 检查项目状态
  2. 查找设计文档
  3. 阅读设计文档
  4. 提出澄清问题
    ↓
使用 writing-plans 创建计划
    ↓
使用 executing-plans 执行
```

---

## 紧急修复流程

如果发现设计与实现不符：

```
1. 立即停止所有修改
2. 重新阅读设计文档
3. 创建偏差分析日志
4. 修正实现
5. 验证每个设计要求
```

---

## 示例

### 正确流程 ✅

```
用户: "执行：添加倒计时闪烁"
    ↓
系统: "检测到执行指令，启动 SUPERPOWER 流程"
    ↓
brainstorming:
  "找到设计文档: DESIGN-UI-001.md"
  "阅读第10.3节：倒计时颜色规范"
  "发现要求：<10秒红色闪烁"
    ↓
writing-plans:
  "创建 Task 4: 添加倒计时闪烁效果"
  "引用设计文档：DESIGN-UI-001.md 第10.3节"
    ↓
executing-plans:
  "执行 Task 4..."
  "验证：闪烁效果正常"
    ↓
完成
```

### 错误流程 ❌（已修复）

```
用户: "修改倒计时"
    ↓
直接编辑代码
    ↓
实现：仅变色
    ↓
用户: "设计与实现完全不符！"
    ↓
浪费大量时间修复
```

---

## 违规处理

如果违反此协议（未经设计检查直接修改代码）：

1. **必须**记录偏差分析日志到 `docs/DEVIATION-ANALYSIS-*.md`
2. **必须**重新执行设计检查流程
3. **必须**修正所有不符合设计的实现
4. **必须**添加回归测试防止再次发生

---

## 工具集成

### IDE 集成（理想）

```bash
# 在 Git commit 前自动检查
git config core.hooks.pre-commit "python -m src.core.pre_execution_check"
```

### VSCode 任务

```json
{
  "before": "python src/core/pre_execution_check.py"
}
```

---

## 当前项目状态

**项目:** exercise-reminder-v2
**主要设计文档:** docs/DESIGN-UI-001.md
**当前待完成任务:**
- Task 4: 添加倒计时<10秒红色闪烁效果
- Task 6: 更新向导测试
- Task 7: 完整集成测试

**未解决的问题:**
- 8个测试失败（需要更新测试以匹配3页向导）
- 倒计时闪烁效果未实现

---

**最后更新:** 2026-01-27
**状态:** 强制执行中
