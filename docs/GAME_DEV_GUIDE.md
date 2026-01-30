# 游戏开发指南

> **用途**：使用 Claude Code + AI 团队进行游戏开发
> **更新日期**：2026-01-19
> **适用引擎**：Godot 4.x

---

## 🎮 核心理念

```
┌─────────────────────────────────────────────────────────┐
│  您（需求方）                                          │
│  ✅ 提供游戏想法和需求                                  │
│  ✅ 测试游戏并提供反馈                                  │
│  ✅ 做设计决策选择                                      │
│  ✅ 复制粘贴文件到真实环境                              │
│  ✅ 处理支付、发布等现实事务                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  AI（开发团队）                                        │
│  ✅ 游戏设计                                            │
│  ✅ 编写所有代码                                        │
│  ✅ 创建场景、节点、资源                                │
│  ✅ 调试和修复问题                                      │
│  ✅ 技术实现指导                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ 可用工具

### 设计组

| 工具 | 角色 | 负责内容 |
|------|------|----------|
| **superpowers: brainstorming** | 游戏设计师 | 游戏玩法创意、机制设计、关卡设计 |
| **superpowers: writing-plans** | 技术策划 | 技术架构、实现计划、任务分解 |
| **frontend-design** | UI/UX 设计师 | 游戏界面、菜单、HUD、交互流程 |

### 开发组

| 工具 | 角色 | 负责内容 |
|------|------|----------|
| **feature-dev** | 功能开发者 | 快速实现功能、编写 GDScript、调试代码 |
| **Godot MCP** | Godot 操作员 | 创建场景、添加节点、配置资源、运行项目 |
| **superpowers: executing** | 项目经理 | 执行开发计划、代码审查、测试验证 |

### 质量组

| 工具 | 角色 | 负责内容 |
|------|------|----------|
| **code-review** | 代码审查员 | 代码质量、性能优化、最佳实践 |
| **superpowers: TDD** | 测试工程师 | 测试用例、功能验证 |

---

## 🔄 完整工作流程

### 阶段 1：游戏概念设计

```
您提出游戏想法
    ↓
调用 choose-tool 技能
    ↓
superpowers: brainstorming
    ↓
细化需求（游戏类型、玩法、美术风格）
    ↓
输出：游戏设计文档
```

### 阶段 2：技术规划

```
设计方案确认
    ↓
superpowers: writing-plans
    ↓
技术架构设计 + 任务分解（2-5分钟/任务）
    ↓
输出：实现计划
```

### 阶段 3：UI/UX 设计

```
需要游戏界面
    ↓
frontend-design
    ↓
设计：主菜单、HUD、设置界面
    ↓
输出：UI 设计稿和代码
```

### 阶段 4：功能开发

```
开发具体功能
    ↓
判断功能复杂度
    ├─ 简单 → feature-dev
    └─ 复杂 → superpowers: executing
    ↓
Godot MCP 创建场景/节点
    ↓
编写 GDScript 代码
    ↓
您复制到 Godot 测试
```

### 阶段 5：质量保证

```
代码完成
    ↓
code-review
    ↓
检查：代码质量、性能
    ↓
您测试反馈
    ↓
有问题 → 修复 → 完成 ✓
```

---

## 📋 工作流程示例

### 场景：制作 2D 平台跳跃游戏

#### 第 1 天：游戏设计

**您说**：
```
"我想做一个类似超级马里奥的 2D 平台游戏"
```

**AI: brainstorming**
```
🎮 正在设计游戏...

请回答：
- 角色有什么特殊能力？
- 敌人类型有哪些？
- 关卡风格？
- 收集品系统？
```

**输出**：
```
docs/plans/2025-01-19-platformer-design.md

📋 游戏设计文档
├── 核心玩法
├── 角色能力
├── 关卡设计
├── UI 设计
└── 技术架构
```

#### 第 2 天：技术规划

**AI: writing-plans**
```
📐 创建实现计划...

场景结构：
├── MainMenu.tscn
├── Game.tscn
│   ├── Player (CharacterBody2D)
│   ├── Level (TileMap)
│   └── Camera2D
└── UI.tscn

任务分解：
1. 创建项目 [2分钟]
2. 玩家移动脚本 [5分钟]
3. 跳跃机制 [3分钟]
4. 碰撞检测 [4分钟]
...
```

#### 第 3-5 天：开发

**AI: feature-dev + Godot MCP**
```
💻 正在开发...

[Godot MCP]
✅ 创建场景: res://scenes/Player.tscn
✅ 添加根节点: CharacterBody2D
✅ 添加子节点: Sprite2D
✅ 添加子节点: CollisionShape2D

[GDScript 代码]
extends CharacterBody2D

const SPEED = 300.0
const JUMP_VELOCITY = -400.0

func _physics_process(delta):
    # 移动逻辑
    ...
```

**您操作**：
1. 复制代码到 `res://scripts/player.gd`
2. 在 Godot 中运行测试
3. 反馈："跳跃高度合适，但移动有点慢"

**AI 调整**：
```
🔧 根据反馈调整...
将 SPEED 从 200.0 改为 300.0
✅ 已更新
```

#### 第 6 天：UI 设计

**AI: frontend-design**
```
🎨 设计游戏界面...

[生成设计稿]
┌─────────────────────────────┐
│        🎮 我的游戏           │
├─────────────────────────────┤
│      [开始游戏]              │
│      [设置]                  │
│      [退出]                  │
└─────────────────────────────┘

✅ 输出：UI 设计 + 实现代码

[Godot MCP 创建 UI 场景]
✅ 创建: res://scenes/MainMenu.tscn
✅ 创建: res://scenes/HUD.tscn
```

#### 第 7 天：测试和优化

**AI: code-review**
```
🔍 代码审查...

检查结果：
✓ 代码质量：良好
✓ 性能：60 FPS 稳定
✓ 最佳实践：遵循 Godot 约定
⚠ 建议：添加对象池优化金币生成

[您决定]
"对象池优化在后续版本"
✅ 已记录到待办事项
```

---

## 🎯 快速开始

### 您的准备

1. **安装 Godot** - https://godotengine.org/download
2. **告诉 AI 您的游戏想法**
3. **准备复制粘贴代码到 Godot**
4. **测试并提供反馈**

### AI 团队会

1. 调用 **choose-tool** 技能
2. 使用 **superpowers** 进行设计和规划
3. 使用 **Godot MCP** 操作 Godot
4. 使用 **feature-dev** 快速开发
5. 等待您测试反馈

---

## 🔧 Godot MCP 配置

### 安装位置
```
F:\claude-code\tools\godot-mcp\
```

### 配置路径
```json
{
  "mcpServers": {
    "godot": {
      "command": "node",
      "args": ["F:\\claude-code\\tools\\godot-mcp\\build\\index.js"],
      "env": {
        "GODOT_PATH": "F:\\godot\\Godot_v4.5.1-stable_win64.exe",
        "DEBUG": "false",
        "READ_ONLY_MODE": "false"
      }
    }
  }
}
```

### Godot MCP 主要功能

- ✅ 启动/控制 Godot 编辑器
- ✅ 创建和修改场景
- ✅ 添加/编辑/删除节点
- ✅ 运行项目并捕获调试输出
- ✅ 项目结构分析

---

## 📚 相关文档

- [工具选择指南](TOOL_SELECTION_GUIDE.md)
- [MCP 服务器列表](mcp/MCP_SERVERS.md)
- [AGENTS.md](../AGENTS.md) - 完整工作流程
- [Superpowers README](../tools/superpowers/README.md)

---

## 💬 常用对话

**开始新游戏项目**：
```
"我想做一个 [游戏类型] 游戏，核心玩法是..."
```

**添加功能**：
```
"给玩家添加 [功能描述] 能力"
```

**调试问题**：
```
"运行时出现错误：[错误信息]"
```

**调整参数**：
```
"[参数] 太大/太小了，调整为 [值]"
```

---

> 💡 **提示**：这个指南适用于所有使用 Claude Code + Godot 的游戏开发项目
