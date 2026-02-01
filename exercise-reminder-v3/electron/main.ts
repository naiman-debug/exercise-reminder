import { app, BrowserWindow } from 'electron';
import path from 'path';
import { getDatabase } from './database/db';
import { DatabaseQueries } from './database/queries';
import { registerIPCHandlers } from './ipc/handlers';
import { ReminderScheduler } from './reminder/scheduler';
import { registerTray } from './tray';

let mainWindow: BrowserWindow | null = null;
let scheduler: ReminderScheduler | null = null;
let isQuitting = false;

const installSafeConsole = () => {
  const wrap = (fn: (...args: any[]) => void) => (...args: any[]) => {
    try {
      fn(...args);
    } catch (error: any) {
      if (error?.code !== 'EPIPE') {
        throw error;
      }
    }
  };

  console.log = wrap(console.log.bind(console));
  console.info = wrap(console.info.bind(console));
  console.warn = wrap(console.warn.bind(console));
  console.error = wrap(console.error.bind(console));
};

installSafeConsole();

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
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist-renderer/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(async () => {
  // 开发模式：加载 React DevTools
  if (process.env.NODE_ENV === 'development') {
    try {
      const installer = require('electron-devtools-installer');
      await installer.default({
        id: 'fmkadmapgofadopljbjfkapdkoienihi',
        electron: '>=1.2.7'
      }, true);
      console.log('[Main] React DevTools installed');
    } catch (error) {
      console.log('[Main] React DevTools already installed or failed:', error);
    }
  }

  createWindow();

  // 初始化数据库
  console.log('[Main] Initializing database...');
  const db = getDatabase();
  const queries = new DatabaseQueries(db);
  console.log('[Main] Database initialized');

  // 创建并启动调度器
  console.log('[Main] Creating scheduler...');
  scheduler = new ReminderScheduler(queries, () => mainWindow);

  // 注册 IPC 处理器（传入调度器）
  console.log('[Main] Registering IPC handlers...');
  if (scheduler) {
    registerIPCHandlers(scheduler);
  }

  // 启动调度器
  console.log('[Main] Starting scheduler...');
  scheduler.start().then(() => {
    console.log('[Main] Scheduler started');

    // 注册系统托盘（需要在调度器启动后）
    if (scheduler) {
      registerTray(mainWindow, scheduler);
    }
  }).catch((error) => {
    console.error('[Main] Failed to start scheduler:', error);
  });
});

app.on('before-quit', () => {
  isQuitting = true;
});

app.on('window-all-closed', () => {
  // macOS: 应用保持运行，点击 Dock 图标时创建新窗口
  if (process.platform !== 'darwin') {
    // 其他平台: 停止调度器并退出
    if (scheduler) {
      console.log('[Main] Stopping scheduler...');
      scheduler.stop();
    }
    // 关闭数据库
    const { closeDatabase } = require('./database/db');
    closeDatabase();
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

export { mainWindow, scheduler };
