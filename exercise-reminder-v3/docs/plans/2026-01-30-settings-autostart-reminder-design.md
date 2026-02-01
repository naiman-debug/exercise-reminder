# 设置页全局保存与开机自启动 - 设计

> **日期**：2026-01-30
> **范围**：设置页（提醒设置全局保存、运动库开机自启动）

## 背景
当前实现的设置页与原型存在两处偏差：
1) 提醒设置为“每卡片确认”，而原型为全局“保存设置”。
2) 运动库缺少“开机自启动”开关（需真实系统开机自启）。

## 目标
- 提醒设置改为“全局一次性保存”，对齐原型页脚按钮。
- 运动库新增“开机自启动”开关，真实接入系统登录项，并持久化。

## 非目标
- 不更改其他页面结构或视觉风格。
- 不引入新的提醒类型。

## 方案概要
### 提醒设置（全局保存）
- 前端保留 `draftSettings` 作为唯一可编辑状态源。
- 用户编辑任意字段仅更新 `draftSettings`。
- 页脚“保存设置”一次性提交全部提醒设置。
- 保存成功后刷新 store 并提示成功；失败则提示并保留用户输入。
- 移除提醒设置卡片内的单独“确认”按钮，避免双入口。

### 开机自启动（真实系统）
- 主进程使用 `app.setLoginItemSettings` 配置系统开机自启。
- 状态持久化到 `system_settings` 表，键：`auto_start_enabled`。
- 提供 IPC：
  - `get-auto-start` 读取系统+持久化状态
  - `set-auto-start` 写入系统设置并持久化
- 前端 Settings 页面“运动库”新增 toggle：
  - 初始值来自 store（IPC 获取）
  - 用户切换时调用 IPC，失败时回滚开关并提示

## 错误处理
- 保存提醒设置失败：弹出错误提示，保留草稿不丢失。
- 设置开机自启动失败：提示失败并回滚 UI 状态。
- 系统不支持开机自启：提示不支持，避免崩溃。

## 测试策略
- 前端：
  - 提醒设置保存触发“批量更新”逻辑
  - 开机自启动 toggle 调用 IPC、失败回滚
- 后端（Electron 主进程/DB）：
  - IPC 读写系统设置
  - `system_settings` 持久化正确

## 涉及文件（预估）
- `src/pages/Settings.tsx`
- `src/store/useSettingsStore.ts`
- `src/types/index.ts`（如需新增类型）
- `electron/ipc/channels.ts`
- `electron/ipc/handlers.ts`
- `electron/preload.ts`
- `electron/database/queries.ts`
- `electron/main.ts`（或新增 autostart 服务）

## 里程碑
1. OpenSpec 变更提案
2. 通过审批后编写实现计划
3. TDD 逐步实现与测试
