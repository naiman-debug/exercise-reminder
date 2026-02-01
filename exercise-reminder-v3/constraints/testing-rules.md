# 测试规则

> **项目**：exercise-reminder-v3
> **版本**：v1.0
> **创建日期**：2026-01-30
> **适用范围**：所有开发任务

---

## 🎯 目的

确保所有代码在完成后经过充分测试验证，提高代码质量和稳定性。

---

## 📌 规则 1：强制测试触发条件

### 必须测试的场景

以下场景**必须立即执行**测试验证：

| 场景 | 说明 | 示例 |
|------|------|------|
| **完成完整模块** | 完成一个功能模块的所有代码 | 数据库层、IPC 通信层、UI 组件 |
| **修改多个文件** | 连续修改超过 3 个文件 | 5 个文件的数据库层 |
| **修复 Bug** | 任何 bug 修复后 | 修复崩溃问题、逻辑错误 |
| **添加新功能** | 任何功能实现后 | 新增用户登录、新增设置选项 |

### 执行时机

```
IF 完成以上任一场景 THEN
    立即执行测试流程
    不允许延迟或跳过
END IF
```

---

## 📌 规则 2：必须使用的 Skills

### 2.1 核心测试 Skills

| Skill | 类型 | 适用场景 | 触发条件 |
|-------|------|----------|----------|
| `test-driven-development` | **强制** | 所有模块 | 完成任何开发后 |
| `security-review` | **强制** | 安全相关 | 处理用户输入、认证、API、敏感数据 |
| `backend-patterns` | **强制** | 后端代码 | API 路由、数据库查询、服务层 |
| `requesting-code-review` | 推荐 | 重大功能 | 提交前审查 |

### 2.2 Skill 使用流程

```bash
# 1. 强制调用测试驱动开发
/skill test-driven-development

# 2. 根据模块类型调用其他 skills
# 安全相关代码
/skill security-review

# 后端代码
/skill backend-patterns

# 重大功能（推荐）
/skill requesting-code-review
```

---

## 📌 规则 3：测试执行标准

### 3.1 单元测试

```bash
# 运行所有测试
npm test

# 检查覆盖率
npm run test:coverage

# 预期结果：
# - 所有测试通过（100%）
# - 覆盖率 >= 80%
```

### 3.2 类型检查

```bash
# TypeScript 类型检查
npx tsc --noEmit

# 预期结果：
# - 无类型错误
```

### 3.3 代码规范

```bash
# ESLint 检查
npm run lint

# 预期结果：
# - 无警告或错误
```

### 3.4 构建验证

```bash
# 构建项目
npm run build

# 预期结果：
# - 构建成功
# - 无构建错误
```

---

## 📌 规则 4：测试通过标准

### 标准通过条件

| 检查项 | 通过标准 |
|--------|----------|
| 单元测试 | ✅ 100% 通过（0 失败） |
| 类型检查 | ✅ 无 TypeScript 错误 |
| 代码规范 | ✅ 无 ESLint 警告 |
| 安全审查 | ✅ 无安全漏洞 |
| 构建验证 | ✅ 构建成功 |
| 代码审查 | ✅ 审查通过（如适用） |

### 不合格处理

```
IF 任何检查项失败 THEN
    1. 记录失败的检查项
    2. 分析失败原因
    3. 修复问题
    4. 重新执行所有检查
    5. 直到全部通过

    ⚠️ 不允许：
    - 跳过失败的检查
    - 标记为"临时完成"
    - 延迟修复
END IF
```

---

## 📌 规则 5：测试报告格式

### 标准报告格式

```markdown
### 🧪 测试验证报告

#### 基本信息
- **时间**：2026-01-30 15:30
- **测试模块**：数据库层（Database Layer）
- **测试类型**：单元测试 / 安全审查 / 架构审查
- **测试文件**：schema.ts, db.ts, queries.ts

#### 测试结果
| 测试项 | 状态 | 说明 |
|--------|------|------|
| 单元测试 | ✅ 通过 | 15/15 tests passed, 95% coverage |
| 类型检查 | ✅ 通过 | No TypeScript errors |
| 代码规范 | ✅ 通过 | No ESLint warnings |
| 安全审查 | ✅ 通过 | No SQL injection vulnerabilities |
| 架构审查 | ✅ 通过 | Follows backend patterns |
| 构建验证 | ✅ 通过 | Build successful |

#### 使用的 Skills
- test-driven-development
- security-review
- backend-patterns

#### 问题记录
（如有问题，记录在这里）

#### 结论
✅ **测试全部通过，模块已完成**

#### 下一步
- 更新 WORK-LOG.md
- 开始下一个模块开发
```

### 简化报告格式（用于小任务）

```markdown
### 🧪 测试报告
- **时间**：[HH:MM]
- **测试**：✅ 全部通过
- 测试：15/15 passed
- 类型：无错误
- Lint：无警告
```

---

## 📌 规则 6：特定模块测试要求

### 6.1 数据库模块

**必须执行**：
- ✅ SQL 注入测试（security-review）
- ✅ 事务测试（test-driven-development）
- ✅ 连接池测试（test-driven-development）
- ✅ 迁移测试（test-driven-development）

### 6.2 API 路由

**必须执行**：
- ✅ 输入验证测试（security-review）
- ✅ 认证测试（security-review）
- ✅ 错误处理测试（test-driven-development）
- ✅ 性能测试（test-driven-development）

### 6.3 IPC 通信

**必须执行**：
- ✅ 消息序列化测试（test-driven-development）
- ✅ 错误传播测试（test-driven-development）
- ✅ 安全检查（security-review）

### 6.4 UI 组件

**必须执行**：
- ✅ 渲染测试（test-driven-development）
- ✅ 用户交互测试（test-driven-development）
- ✅ 可访问性测试（test-driven-development）

---

## 📌 规则 7：Bug 修复测试

### 修复验证流程

```
1. 理解 Bug
   ├─ 阅读 Bug 报告
   ├─ 复现 Bug
   └─ 确定根本原因

2. 修复 Bug
   ├─ 编写修复代码
   └─ 编写/更新测试用例

3. 验证修复
   ├─ 运行相关测试
   ├─ 复现 Bug（应不再出现）
   ├─ 检查是否引入新问题
   └─ 使用 test-driven-development skill

4. 记录修复
   └─ 更新 BUG-QUESTION-LOG.md
```

### Bug 修复报告格式

```markdown
### 🐛 Bug 修复报告

#### Bug 信息
- **Bug ID**：BUG-001
- **描述**：[简要描述]
- **严重程度**：P0/P1/P2

#### 修复内容
- **修改文件**：`path/to/file.ts:42`
- **修复说明**：[详细说明]

#### 验证结果
| 检查项 | 状态 |
|--------|------|
| Bug 不再出现 | ✅ |
| 相关测试通过 | ✅ |
| 无新问题 | ✅ |

#### 使用的 Skills
- test-driven-development
- systematic-debugging（如需要）
```

---

## 📌 规则 8：持续集成

### CI 检查点

每次提交前必须确保：

```bash
# 1. 运行所有测试
npm test

# 2. 类型检查
npm run type-check

# 3. 代码规范
npm run lint

# 4. 构建验证
npm run build

# 5. 安全审查（如适用）
/skill security-review
```

### 提交前检查清单

- [ ] 所有测试通过
- [ ] 无类型错误
- [ ] 无 Lint 警告
- [ ] 构建成功
- [ ] 安全审查通过（如适用）
- [ ] 代码审查通过（如适用）
- [ ] 更新相关文档

---

## 📌 规则 9：测试覆盖率目标

### 覆盖率要求

| 模块类型 | 最低覆盖率 | 推荐覆盖率 |
|----------|-----------|-----------|
| 核心业务逻辑 | 90% | 95%+ |
| API 路由 | 85% | 90%+ |
| 数据库查询 | 90% | 95%+ |
| UI 组件 | 80% | 85%+ |
| 工具函数 | 95% | 100% |

### 检查覆盖率

```bash
# 生成覆盖率报告
npm run test:coverage

# 查看 report
open coverage/index.html
```

---

## 📌 规则 10：测试文档

### 测试文档位置

- **测试计划**：`docs/tests/test-plan.md`
- **测试报告**：`docs/tests/test-reports/YYYY-MM-DD-report.md`
- **覆盖率报告**：`coverage/`

### 测试计划模板

```markdown
# [模块名] 测试计划

## 测试范围
- [功能 1]
- [功能 2]

## 测试用例
### TC-001: [测试用例名称]
- **目标**：[测试目标]
- **步骤**：[测试步骤]
- **预期**：[预期结果]

## 测试数据
- [测试数据说明]

## 测试环境
- Node 版本：
- 依赖版本：
```

---

## 🔗 相关文档

- **工作流恢复**：[workflow-recovery.md](./workflow-recovery.md)
- **约束目录**：[README.md](./README.md)
- **工作日志**：`../docs/WORK-LOG.md`
- **Bug 日志**：`../docs/BUG-QUESTION-LOG.md`

---

## 📝 版本历史

- **v1.0** (2026-01-30) - 初始版本
  - 定义 10 条核心测试规则
  - 规范测试触发条件和流程
  - 定义测试通过标准
  - 建立测试报告格式

---

> ⚠️ **重要提示**：测试不是可选项，是强制要求！
>
> 每次完成开发后，必须立即执行测试验证。不允许跳过测试或标记为"临时完成"。
