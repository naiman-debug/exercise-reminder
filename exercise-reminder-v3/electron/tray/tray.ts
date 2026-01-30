import { Tray, Menu, nativeImage, BrowserWindow, NativeImage } from 'electron';
import path from 'path';
import { ReminderScheduler } from '../reminder/scheduler';

/**
 * 系统托盘管理器
 * 负责创建和管理系统托盘图标和菜单
 */
export class TrayManager {
  private tray: Tray | null = null;
  private isPaused: boolean = false;

  constructor(
    private scheduler: ReminderScheduler,
    private getMainWindow: () => BrowserWindow | null
  ) {}

  /**
   * 创建系统托盘
   */
  create(): void {
    if (this.tray) {
      console.log('[TrayManager] Tray already exists');
      return;
    }

    console.log('[TrayManager] Creating tray...');

    // 加载托盘图标（开发模式使用临时图标，生产模式使用打包后的图标）
    const icon = this.getTrayIcon();

    this.tray = new Tray(icon);
    this.tray.setToolTip('健康提醒助手');

    // 设置右键菜单
    this.updateMenu();

    // 点击托盘图标显示主窗口
    this.tray.on('click', () => {
      this.showMainWindow();
    });

    console.log('[TrayManager] Tray created successfully');
  }

  /**
   * 获取托盘图标
   */
  private getTrayIcon(): NativeImage {
    // 尝试加载图标文件
    const iconPaths = [
      path.join(__dirname, '../../assets/tray-icon.png'),
      path.join(__dirname, '../../assets/tray-icon.ico'),
      path.join(__dirname, '../assets/tray-icon.png'),
    ];

    if (process.env.NODE_ENV === 'development') {
      // 开发模式：尝试多个可能的路径
      for (const iconPath of iconPaths) {
        try {
          const image = nativeImage.createFromPath(iconPath);
          if (!image.isEmpty()) {
            return image.resize({ width: 16, height: 16 });
          }
        } catch {
          continue;
        }
      }
      // 如果所有图标文件都不存在，创建一个简单的占位图标
      console.warn('[TrayManager] No tray icon found, using placeholder');
      return this.createPlaceholderIcon();
    } else {
      // 生产模式：使用打包后的图标
      const iconPath = path.join(process.resourcesPath, 'assets', 'tray-icon.png');
      try {
        return nativeImage.createFromPath(iconPath).resize({ width: 16, height: 16 });
      } catch {
        console.warn('[TrayManager] Production icon not found, using placeholder');
        return this.createPlaceholderIcon();
      }
    }
  }

  /**
   * 创建占位图标（简单的紫色圆圈）
   */
  private createPlaceholderIcon(): NativeImage {
    // 创建一个 16x16 的简单图标
    const size = 16;
    const buffer = Buffer.alloc(size * size * 4);

    // 填充紫色像素（RGBA: #7C3AED -> R=124, G=58, B=237, A=255）
    for (let i = 0; i < size * size; i++) {
      const idx = i * 4;
      buffer[idx] = 124;     // R
      buffer[idx + 1] = 58;  // G
      buffer[idx + 2] = 237; // B
      buffer[idx + 3] = 255; // A
    }

    return nativeImage.createFromBuffer(buffer, { width: size, height: size });
  }

  /**
   * 更新托盘菜单
   */
  updateMenu(): void {
    if (!this.tray) return;

    const pauseResumeText = this.isPaused ? '恢复提醒' : '暂停提醒';
    const pauseResumeEnabled = this.scheduler.getState().isRunning;

    const template: Electron.MenuItemConstructorOptions[] = [
      {
        label: '显示主界面',
        click: () => this.showMainWindow(),
      },
      {
        type: 'separator',
      },
      {
        label: pauseResumeText,
        enabled: pauseResumeEnabled,
        click: () => this.togglePause(),
      },
      {
        label: '设置',
        click: () => this.showSettings(),
      },
      {
        type: 'separator',
      },
      {
        label: '退出',
        click: () => this.quitApp(),
      },
    ];

    const contextMenu = Menu.buildFromTemplate(template);
    this.tray.setContextMenu(contextMenu);
  }

  /**
   * 显示主窗口
   */
  private showMainWindow(): void {
    const mainWindow = this.getMainWindow();
    if (mainWindow) {
      if (mainWindow.isMinimized()) {
        mainWindow.restore();
      }
      mainWindow.show();
      mainWindow.focus();
    } else {
      console.log('[TrayManager] No main window found');
    }
  }

  /**
   * 切换暂停/恢复状态
   */
  private togglePause(): void {
    this.isPaused = !this.isPaused;

    if (this.isPaused) {
      this.scheduler.pause();
      console.log('[TrayManager] Reminders paused');
    } else {
      this.scheduler.resume();
      console.log('[TrayManager] Reminders resumed');
    }

    // 更新托盘图标（可选，区分暂停状态）
    // this.updateTrayIcon();

    // 更新菜单
    this.updateMenu();
  }

  /**
   * 显示设置窗口
   */
  private showSettings(): void {
    // TODO: 实现设置窗口
    console.log('[TrayManager] Show settings (TODO)');
    this.showMainWindow();
  }

  /**
   * 退出应用
   */
  private quitApp(): void {
    console.log('[TrayManager] Quitting app...');
    const { app } = require('electron');
    app.quit();
  }

  /**
   * 更新暂停状态（外部调用）
   */
  setPausedState(isPaused: boolean): void {
    this.isPaused = isPaused;
    this.updateMenu();
  }

  /**
   * 销毁托盘
   */
  destroy(): void {
    if (this.tray) {
      this.tray.destroy();
      this.tray = null;
      console.log('[TrayManager] Tray destroyed');
    }
  }

  /**
   * 获取托盘实例
   */
  getTray(): Tray | null {
    return this.tray;
  }
}
