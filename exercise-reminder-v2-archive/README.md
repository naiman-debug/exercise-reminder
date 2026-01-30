# "灵动休息"健康助手 v2.0

> Windows 桌面久坐提醒应用 - 强制你定时站立、运动、远眺

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 功能特点

### 核心功能
- **三大强制提醒**：站立、微运动、远眺（随机间隔触发）
- **纯倒计时交互**：自动结束，无需按钮操作
- **全屏倒计时**：大字体显示，颜色渐变提醒
- **热量计算**：基于 MET 值科学计算运动消耗

### 辅助功能
- **统计页面**：今日统计 + 7 天热量趋势图
- **首次启动向导**：4 步引导完成初始设置
- **动作库管理**：10 个默认动作，支持自定义
- **呼吸感设计**：柔和有机的视觉体验
- **数据统计**：记录每日活动，生成趋势图

### 技术特性
- **完全本地**：所有数据存储在本地，保护隐私
- **系统托盘**：最小化到托盘，不干扰工作
- **音频提示**：提醒音效 + 可选 TTS 语音播报

## 快速开始

### 安装

1. 克隆仓库
```bash
git clone https://github.com/yourusername/exercise-reminder.git
cd exercise-reminder-v2
```

2. 创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

### 运行

```bash
python src/main.py
```

### 打包

```bash
pyinstaller build.spec
```

## 项目结构

```
exercise-reminder-v2/
├── docs/              # 设计文档
│   ├── PRD-v2.0.md              # 产品需求文档 (v2.0)
│   ├── DESIGN-IxD-001.md        # 交互设计
│   ├── DESIGN-UI-001.md         # 页面设计
│   └── DESIGN-ARCH-001.md       # 技术架构
├── src/               # 源代码
│   ├── core/         # 核心业务逻辑
│   │   └── reminder_engine.py    # 提醒引擎
│   ├── models/       # 数据模型
│   │   ├── models.py             # Peewee ORM 模型
│   │   ├── repositories.py       # 数据仓储层
│   │   └── database.py           # 数据库管理
│   ├── ui/           # UI 组件
│   │   ├── dialogs/              # 提醒弹窗
│   │   ├── wizards/              # 首次启动向导
│   │   ├── settings/             # 设置对话框
│   │   ├── design/               # 呼吸感设计系统
│   │   └── main_window.py        # 主窗口
│   └── utils/        # 工具函数
│       ├── logger.py             # 日志系统 (loguru)
│       ├── audio_player.py       # 音频播放
│       └── met_calculator.py     # MET 热量计算
├── data/             # 数据目录（运行时创建）
├── tests/            # 测试代码
├── docs/             # 文档
├── requirements.txt   # 依赖清单
└── pyproject.toml    # 项目配置
```

## 技术栈

- **GUI**: PySide6 (Qt for Python 6.x)
- **数据库**: SQLite + Peewee ORM
- **日志**: loguru
- **测试**: pytest + pytest-qt
- **图表**: matplotlib (待集成)

## 开发

### 运行测试

```bash
pytest tests/
```

**当前测试覆盖**：91/91 通过 ✅

### 代码风格

遵循 PEP 8 规范，使用 4 空格缩进。

## 文档

- [产品需求文档 v2.0](docs/PRD-v2.0.md)
- [交互设计文档](docs/DESIGN-IxD-001.md)
- [页面设计文档](docs/DESIGN-UI-001.md)
- [技术架构文档](docs/DESIGN-ARCH-001.md)

## v2.0 更新内容

### 新增功能 ✨
- ✅ 统计页面（今日统计 + 7 天趋势图）
- ✅ 呼吸感设计系统（DesignTokens）
- ✅ 首次启动向导（4 页流程）
- ✅ 完成反馈显示热量消耗

### 优化改进 🔧
- ✅ 去掉惩罚机制（更友好的体验）
- ✅ 所有提醒改为纯倒计时自动结束
- ✅ 延长完成反馈时间到 1 秒
- ✅ 统一的日志系统（loguru）

### 待完成功能 🚧
- ⏳ 统计图表可视化（matplotlib 集成）
- ⏳ 提醒冷却机制（2 分钟）
- ⏳ 动作库 CRUD 界面
- ⏳ TTS 语音播报集成

## 许可证

MIT License

## 作者

Claude Code

## 致谢

感谢所有为开源社区贡献的开发者。
