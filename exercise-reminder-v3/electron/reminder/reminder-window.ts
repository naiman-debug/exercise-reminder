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
    if (this.reminderWindow && !this.reminderWindow.isDestroyed()) {
      this.reminderWindow.close();
    }

    this.reminderWindow = this.createReminderWindow(eventData);
    this.loadReminderContent(eventData);
  }

  /**
   * 创建提醒窗口（无边框）
   */
  private createReminderWindow(eventData: TriggerEvent): BrowserWindow {
    const isStandReminder = eventData.type === 'stand';
    const windowWidth = isStandReminder ? 450 : 720;
    const windowHeight = isStandReminder ? 360 : 480;

    const window = new BrowserWindow({
      width: windowWidth,
      height: windowHeight,
      useContentSize: true,
      frame: false,
      transparent: true,
      backgroundColor: '#00000000',
      alwaysOnTop: true,
      skipTaskbar: false,
      resizable: false,
      movable: true,
      minimizable: true,
      maximizable: false,
      closable: true,
      title: this.getWindowTitle(eventData.type),
      titleBarStyle: 'hidden',
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, '../dist-electron/preload.js'),
      },
    });

    const display = screen.getPrimaryDisplay();
    const workArea = display.workAreaSize;
    const x = Math.floor((workArea.width - windowWidth) / 2);
    const y = Math.floor((workArea.height - windowHeight) / 2);
    window.setPosition(x, y);

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
        return '微运动时间';
      case 'gaze':
        return '远眺放松';
      case 'stand':
        return '站立提醒';
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
