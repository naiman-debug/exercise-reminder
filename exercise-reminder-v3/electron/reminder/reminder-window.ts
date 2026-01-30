import { BrowserWindow, screen } from 'electron';
import path from 'path';
import { TriggerEvent } from './types';

/**
 * 提醒弹窗管理器
 * 负责创建和管理提醒窗口
 */
export class ReminderWindowManager {
  private reminderWindow: BrowserWindow | null = null;

  /**
   * 显示提醒窗口
   */
  showReminder(eventData: TriggerEvent): void {
    // 如果已有提醒窗口，先关闭
    if (this.reminderWindow && !this.reminderWindow.isDestroyed()) {
      this.reminderWindow.close();
    }

    // 创建提醒窗口
    this.reminderWindow = this.createReminderWindow(eventData);

    // 加载内容
    this.loadReminderContent(eventData);
  }

  /**
   * 创建提醒窗口
   */
  private createReminderWindow(eventData: TriggerEvent): BrowserWindow {
    const display = screen.getPrimaryDisplay();
    const workArea = display.workAreaSize;

    // 站立提醒使用小窗口（60% 大小）
    const isStandReminder = eventData.type === 'stand';
    const windowWidth = isStandReminder ? Math.floor(workArea.width * 0.35) : Math.floor(workArea.width * 0.5);
    const windowHeight = isStandReminder ? Math.floor(workArea.height * 0.4) : Math.floor(workArea.height * 0.6);

    const window = new BrowserWindow({
      width: windowWidth,
      height: windowHeight,
      frame: true, // 显示窗口边框和标题栏
      transparent: false,
      alwaysOnTop: true,
      skipTaskbar: false,
      resizable: true,
      movable: true,
      minimizable: true,
      maximizable: false,
      closable: true,
      title: this.getWindowTitle(eventData.type),
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, '../dist-electron/preload.js'),
      },
    });

    // 居中显示
    window.center();

    // 窗口关闭时清理引用
    window.on('closed', () => {
      this.reminderWindow = null;
    });

    return window;
  }

  /**
   * 获取窗口标题
   */
  private getWindowTitle(type: string): string {
    switch (type) {
      case 'exercise':
        return '🏃 微运动时间';
      case 'gaze':
        return '👀 远眺放松';
      case 'stand':
        return '🧍 站立提醒';
      default:
        return '健康提醒';
    }
  }

  /**
   * 加载提醒内容
   */
  private loadReminderContent(eventData: TriggerEvent): void {
    if (!this.reminderWindow) return;

    const params = new URLSearchParams({
      type: eventData.type,
      duration: eventData.duration.toString(),
      ...(eventData.exerciseName && { exerciseName: eventData.exerciseName }),
      ...(eventData.metValue && { metValue: eventData.metValue.toString() }),
    });

    if (process.env.NODE_ENV === 'development') {
      this.reminderWindow.loadURL(`http://localhost:5173/#/reminder?${params.toString()}`);
      // 开发模式打开 DevTools
      // this.reminderWindow.webContents.openDevTools();
    } else {
      this.reminderWindow.loadURL(`file://${path.join(__dirname, '../dist-renderer/index.html')}#/reminder?${params.toString()}`);
    }
  }

  /**
   * 关闭提醒窗口
   */
  closeReminder(): void {
    if (this.reminderWindow && !this.reminderWindow.isDestroyed()) {
      this.reminderWindow.close();
      this.reminderWindow = null;
    }
  }

  /**
   * 最小化提醒窗口
   */
  minimizeReminder(): void {
    if (this.reminderWindow && !this.reminderWindow.isDestroyed()) {
      this.reminderWindow.minimize();
    }
  }

  /**
   * 获取提醒窗口
   */
  getWindow(): BrowserWindow | null {
    return this.reminderWindow;
  }
}
