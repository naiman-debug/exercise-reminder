# Bug 和问题解决记录

> exercise-reminder-v3 项目问题解决日志
> 记录所有 bug 和技术问题的完整排查过程

---

## 📋 目录

1. [Bug 记录](#bug-记录)
2. [技术问题记录](#技术问题记录)
3. [经验教训](#经验教训)

---

## Bug 记录
### Bug #005: 设置页保存后无法再次编辑/点击

**发现时间**：2026-01-31

**严重程度**：🟠 P1

**问题描述**：
- 在设置页点击“保存设置”后，当前页所有输入框与 Tab 按钮无法再次点击
- 必须返回首页再进入设置页，才能恢复编辑

**根本原因**：
- 使用 `window.alert` 作为保存反馈，在 Electron 渲染进程中会触发阻塞式模态对话框
- 关闭后出现交互被遮罩的现象，导致点击失效

**解决方案**：
- 移除 `alert` 保存提示
- 改为页面内非阻塞状态提示（toast/提示条）

**经验教训**：
- Electron 渲染进程避免使用 `alert/confirm` 作为交互反馈
- 保存反馈应使用非阻塞 UI

### Bug #006: 提醒弹窗仍显示系统边框/菜单

**发现时间**：2026-01-31

**严重程度**：🟡 P2

**问题描述**：
- 提醒弹窗仍显示系统菜单栏（File/Edit/View）
- 弹窗尺寸看起来比设计更大

**根本原因**：
- dev 模式使用 `dist-electron` 主进程代码
- 未重新编译 `electron/reminder/reminder-window.ts`，导致旧版 `frame: true` 仍在运行

**解决方案**：
- 在 `dev:electron` 脚本中增加 `npm run build:main`
- 重启 dev 进程后生效

**经验教训**：
- 修改主进程代码后必须先编译，再启动 Electron

### Bug #007: 今日活动与历史数据不更新

**发现时间**：2026-01-31

**严重程度**：🟠 P1

**问题描述**：
- 首页“今日活动详情”长期为空
- 历史累计消耗（大卡）不更新

**根本原因**：
- 提醒完成时保存活动缺少 `timestamp/date/completed` 等关键字段
- `daily_stats` 未在每次活动保存后更新，历史统计取不到最新值

**解决方案**：
- 在提醒弹窗保存活动时补齐 `timestamp/date/weight/calories/completed`
- 在 `DatabaseQueries.saveActivity` 中同步更新 `daily_stats`

**经验教训**：
- 写入活动记录必须包含时间与日期字段
- 历史统计依赖 daily_stats 时要确保每次活动都同步更新

### Bug #004: 主进程日志写入触发 EPIPE 崩溃

**发现时间**：2026-01-30

**严重程度**：🟠 P1

**问题描述**：
- 触发提醒时主进程弹出错误：Error: EPIPE: broken pipe, write
- 堆栈指向 ReminderScheduler.handleTrigger 的 console.log

**根本原因**：
- 在无控制台或 stdout 关闭的环境中，console.log 写入触发 EPIPE

**解决方案**：
- 在 electron/main.ts 里安装安全日志包装器，捕获并忽略 EPIPE
### Bug #002: 提醒弹窗内容空白（带查询参数的 hash 路由无法匹配）

**发现时间**：2026-01-30

**严重程度**：🟠 P1

**问题描述**：
- 站立提醒弹窗出现空白内容（仅显示窗口边框）
- URL 形如 #/reminder?type=stand&duration=300 时路由未命中

**根本原因**：
- App.tsx 直接用完整 hash 匹配路由，未剥离查询参数

**解决方案**：
- 统一 hash 解析并忽略查询参数
- 补充路由解析单元测试

### Bug #003: 提醒设置缺少确认按钮

**发现时间**：2026-01-30

**严重程度**：🟡 P2

**问题描述**：
- 提醒设置页修改运动/远眺/站立间隔后没有“确认/保存”操作

**解决方案**：
- 增加草稿态编辑并提供“确认”按钮提交更新

### Bug #001: 设置页面和运动库页面显示空白

**发现时间**：2026-01-30

**严重程度**：🔴 P0 - 阻塞

**问题描述**：
- 设置页面的"提醒设置"内容区域完全空白
- 运动库页面显示空白
- 添加运动按钮点击无反应

**排查过程**：

1. **初步检查**：
   - 检查前端组件代码，渲染逻辑正常
   - 检查 API 调用，发现 `window.electronAPI` 存在

2. **控制台错误**：
   - 无明显错误信息
   - 网络请求无响应

3. **使用 Skills 专业审查**：
   - test-driven-development：编写单元测试发现 API 调用失败
   - security-review：检查 IPC 通信安全
   - backend-patterns：审查后端架构

4. **根本原因发现**：
   ```bash
   # 检查编译后的 main.js
   cat dist-electron/main.js
   ```

   发现 `main.ts` 缺少关键初始化代码！

**根本原因**：

1. **主进程未初始化关键模块**：
   ```typescript
   // 错误的 main.ts（修复前）
   app.whenReady().then(createWindow);

   // 缺少：
   // - 数据库初始化
   // - IPC 处理器注册
   // - 调度器启动
   // - 系统托盘注册
   ```

2. **数据库列名不匹配**：
   ```typescript
   // 数据库列名：snake_case
   CREATE TABLE reminder_settings (
     interval_min INTEGER,
     interval_max INTEGER,
     ...
   );

   // TypeScript 接口：camelCase
   interface ReminderSettings {
     intervalMin: number;
     intervalMax: number;
   }

   // 查询时没有列名别名
   return this.db.prepare('SELECT * FROM reminder_settings').all() as ReminderSettings[];
   // 结果：intervalMin 和 intervalMax 都是 undefined！
   ```

**解决方案**：

1. **修复 main.ts**：
   ```typescript
   app.whenReady().then(() => {
     createWindow();

     // 1. 初始化数据库
     const db = getDatabase();
     const queries = new DatabaseQueries(db);

     // 2. 创建调度器
     scheduler = new ReminderScheduler(queries, () => mainWindow);

     // 3. 注册 IPC 处理器
     if (scheduler) {
       registerIPCHandlers(scheduler);
     }

     // 4. 启动调度器
     scheduler.start().then(() => {
       // 5. 注册系统托盘
       if (scheduler) {
         registerTray(mainWindow, scheduler);
       }
     });
   });
   ```

2. **修复数据库查询（queries.ts）**：
   ```typescript
   // 添加列名别名
   getReminderSettings(): ReminderSettings[] {
     return this.db.prepare(`
       SELECT
         id, type,
         interval_min as intervalMin,
         interval_max as intervalMax,
         duration,
         enabled,
         updated_at as updatedAt
       FROM reminder_settings
     `).all() as ReminderSettings[];
   }

   // 同样修复所有其他查询：
   // - getUserInfo
   // - getAllExercises
   // - getActivitiesByDate
   // - getRecentActivities
   ```

3. **删除旧数据库文件**：
   ```bash
   rm -f "C:/Users/Administrator/AppData/Roaming/health-reminder/health-reminder.db"*
   ```

4. **重新编译**：
   ```bash
   npm run build:main
   npm run dev
   ```

**验证**：
```
[ReminderScheduler] Loaded exercise settings: 10-20min, 120s  ✅
[ReminderScheduler] Loaded gaze settings: 10-20min, 60s     ✅
[ReminderScheduler] Loaded stand settings: 10-20min, 300s    ✅
```

**经验教训**：
- ✅ 主进程启动时必须按正确顺序初始化所有模块
- ✅ 数据库查询永远不要用 `SELECT *` + 类型断言
- ✅ 使用专业 Skills 工具比手动排查更高效
- ✅ 编写单元测试能快速发现问题根源

---

### Bug #002: Electron 模块文件锁定

**发现时间**：2026-01-30 晚间

**严重程度**：🟡 P1 - 影响开发

**问题描述**：
```
EBUSY: resource busy or locked
node_modules/electron 文件被系统锁定
```

**排查过程**：

1. 尝试重新安装 electron：
   ```bash
   npm install electron@^33.4.11 --save-dev
   ```
   失败：文件被锁定

2. 检查占用进程：
   ```bash
   netstat -ano | findstr :5173
   ```
   发现 Electron 进程仍在运行

3. 尝试终止进程：
   ```bash
   taskkill /F /PID <进程ID>
   ```

**根本原因**：
- Electron 应用在后台运行
- Windows 文件系统锁定机制

**解决方案**：
1. 重启电脑（最可靠）
2. 或手动终止所有 Electron 进程

**经验教训**：
- ⚠️ 修改 Electron 代码后必须完全重启应用
- ⚠️ npm run dev 后台运行，需要手动终止

---

### Bug #003: 提醒设置加载为 undefined

**发现时间**：2026-01-30（修复 Bug #001 时发现）

**严重程度**：🟡 P1

**问题描述**：
```
[ReminderScheduler] Loaded exercise settings: undefined-undefinedmin, 120s
```

**排查过程**：

检查 `getReminderSettings` 返回值：
```typescript
const settings = this.queries.getReminderSettings();
console.log(settings);
// 输出：[{id: 1, type: 'exercise', interval_min: 10, interval_max: 20, ...}]
//      注意：interval_min 不是 intervalMin！
```

**根本原因**：
数据库列名是 `interval_min`（snake_case），但 TypeScript 接口期望 `intervalMin`（camelCase）

**解决方案**：见 Bug #001

**经验教训**：
- ✅ 数据库设计时统一命名规范（推荐 snake_case）
- ✅ 查询时添加列名别名
- ✅ 不要依赖 `as` 类型断言来"修复"类型不匹配

---

## 技术问题记录

### 问题 #001: better-sqlite3 编译问题

**时间**：2026-01-30

**问题描述**：
```
gyp info it worked if it ends with ok
gyp info it worked if it ends with ok
但 electron 启动时报错找不到模块
```

**解决方案**：
```bash
# 重新构建原生模块
npm rebuild better-sqlite3

# 或使用 electron-rebuild
npx electron-rebuild -f -w better-sqlite3
```

**经验教训**：
- Electron 需要特定版本的原生模块
- 修改 Node 版本或 Electron 版本后需要重新编译

---

### 问题 #002: Vite 端口占用

**时间**：2026-01-30

**问题描述**：
```
Error: Port 5173 is already in use
```

**解决方案**：
```bash
# 查找占用进程
netstat -ano | findstr :5173

# 终止进程
taskkill /F /PID <进程ID>
```

**经验教训**：
- 开发服务器后台运行，需要正确终止
- 可以使用 `concurrently` 统一管理

---

### 问题 #003: TypeScript 类型断言掩盖 bug

**时间**：2026-01-30

**问题描述**：
```typescript
// 看起来正确，实际运行时出错
return this.db.prepare('SELECT * FROM reminder_settings').all() as ReminderSettings[];
// intervalMin 是 undefined，但 TypeScript 不会报错
```

**解决方案**：
```typescript
// 方法 1：添加列名别名（推荐）
return this.db.prepare(`
  SELECT interval_min as intervalMin, ...
FROM reminder_settings
`).all() as ReminderSettings[];

// 方法 2：定义精确的数据库类型
interface ReminderSettingsRow {
  interval_min: number;
  interval_max: number;
  ...
}
function transform(row: ReminderSettingsRow): ReminderSettings {
  return {
    intervalMin: row.interval_min,
    intervalMax: row.interval_max,
    ...
  };
}
```

**经验教训**：
- ❌ 不要用 `as` 类型断言"修复"类型不匹配
- ✅ 让类型系统真正保护你
- ✅ 数据库查询应该明确指定列名

---

### 问题 #004: IPC 通信失败

**时间**：2026-01-30

**问题描述**：
```typescript
// 前端调用
const result = await window.electronAPI.getReminderSettings();
console.log(result); // undefined
```

**排查过程**：

1. 检查 preload.ts：API 已暴露 ✅
2. 检查 channels.ts：通道名称正确 ✅
3. 检查 handlers.ts：处理器已注册？❌

**根本原因**：
main.ts 中没有调用 `registerIPCHandlers()`

**解决方案**：见 Bug #001

**经验教训**：
- ✅ Electron IPC 必须在主进程中注册处理器
- ✅ 使用检查清单验证所有初始化步骤

---

## 经验教训

### 1. 调试流程

**遇到问题时**：
1. ✅ 先查看控制台错误
2. ✅ 检查相关代码逻辑
3. ✅ 使用专业 Skills 工具审查
4. ✅ 编写单元测试复现问题
5. ❌ 不要盲目修改代码

### 2. TypeScript 最佳实践

**DO ✅**：
```typescript
// 明确指定列名
return this.db.prepare(`
  SELECT col1 as field1, col2 as field2
  FROM table
`).all() as MyType[];
```

**DON'T ❌**：
```typescript
// 不要这样做
return this.db.prepare('SELECT * FROM table').all() as MyType[];
```

### 3. Electron 初始化清单

- [ ] 数据库初始化
- [ ] IPC 处理器注册
- [ ] 调度器启动
- [ ] 系统托盘注册
- [ ] 窗口创建

### 4. 数据库设计规范

- 表名和列名：snake_case（`reminder_settings`）
- TypeScript 接口：camelCase（`ReminderSettings`）
- 查询时添加别名转换

---

## 更新记录

| 日期 | Bug/问题 | 解决方案 | 作者 |
|------|----------|----------|------|
| 2026-01-31 | Bug #007: 活动/历史不更新 | 保存活动补齐字段 + 更新 daily_stats | Claude Code |
| 2026-01-31 | Bug #006: 提醒窗仍有系统边框 | dev 启动前编译主进程 | Claude Code |
| 2026-01-31 | Bug #005: 保存后无法再编辑 | 移除 alert，改为非阻塞提示 | Claude Code |
| 2026-01-30 | Bug #001: 页面空白 | 修复 main.ts 和数据库查询 | Claude Code |
| 2026-01-30 | Bug #002: Electron 锁定 | 重启电脑 | Claude Code |
| 2026-01-30 | Bug #003: 设置 undefined | 添加列名别名 | Claude Code |

---

> **规则**：每次遇到新问题必须立即记录本文档


