// Electron v33+ 使用新的导入路径
const { app, BrowserWindow } = require('electron/main');
const path = require('path');
const { getDatabase } = require('./database/db');
const { DatabaseQueries } = require('./database/queries');
const { registerIPCHandlers } = require('./ipc/handlers');
const { ReminderScheduler } = require('./reminder/scheduler');
const { TrayManager } = require('./tray');

let mainWindow = null;
let scheduler = null;
let trayManager = null;
let isQuitting = false;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, '../dist-electron/preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // 开发模式加载 Vite 服务器，生产模式加载构建文件
  const isDev = process.env.NODE_ENV === 'development' || process.defaultApp || !app.isPackaged;
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
    console.log('[Main] Development mode: loading from Vite dev server');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist-renderer/index.html'));
    console.log('[Main] Production mode: loading from built files');
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // 窗口关闭时最小化到托盘，而不是直接退出
  mainWindow.on('close', (event) => {
    if (!isQuitting && mainWindow && !mainWindow.isMinimized()) {
      // 只有在窗口正常显示时才隐藏到托盘
      // 避免启动时误触发
      event.preventDefault();
      mainWindow.hide();
      console.log('[Main] Window hidden to tray');
    }
  });

  return mainWindow;
}

app.whenReady().then(() => {
  console.log('[Main] App ready, initializing...');

  // 创建主窗口
  mainWindow = createWindow();

  // 初始化数据库
  const db = getDatabase();
  const queries = new DatabaseQueries(db);

  // 初始化调度器
  scheduler = new ReminderScheduler(queries, () => mainWindow);
  console.log('[Main] Scheduler created');

  // 注册 IPC 处理器（传递调度器实例）
  registerIPCHandlers(scheduler);
  console.log('[Main] IPC handlers registered');

  // 启动调度器
  scheduler.start().catch(console.error);
  console.log('[Main] Scheduler started');

  // 初始化系统托盘
  trayManager = new TrayManager(scheduler, () => mainWindow);
  trayManager.create();
  console.log('[Main] Tray initialized');

  // macOS: 当点击 Dock 图标时重新创建窗口
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      mainWindow = createWindow();
    }
  });

  console.log('[Main] App initialization complete');
});

// 所有窗口关闭时的处理（Windows & Linux）
app.on('window-all-closed', () => {
  console.log('[Main] All windows closed');

  // 停止调度器
  if (scheduler) {
    scheduler.stop();
    console.log('[Main] Scheduler stopped');
  }

  // 销毁托盘
  if (trayManager) {
    trayManager.destroy();
    console.log('[Main] Tray destroyed');
  }

  // macOS 下不退出应用
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// 应用退出前的清理
app.on('before-quit', () => {
  console.log('[Main] App quitting...');
  isQuitting = true;

  // 停止调度器
  if (scheduler) {
    scheduler.stop();
  }

  // 销毁托盘
  if (trayManager) {
    trayManager.destroy();
  }
});

// 导出实例供其他模块使用（如果需要）
module.exports = { mainWindow, scheduler, trayManager };
