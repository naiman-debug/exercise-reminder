/**
 * 系统托盘模块
 *
 * 提供系统托盘图标和右键菜单功能
 */

import { TrayManager } from './tray';
import { BrowserWindow } from 'electron';
import { ReminderScheduler } from '../reminder/scheduler';

let trayManager: TrayManager | null = null;

/**
 * 注册系统托盘
 */
export function registerTray(
  mainWindow: BrowserWindow | null,
  scheduler: ReminderScheduler
): void {
  if (trayManager) {
    console.log('[Tray] Tray already registered');
    return;
  }

  console.log('[Tray] Registering tray...');
  trayManager = new TrayManager(scheduler, () => mainWindow);
  trayManager.create();
  console.log('[Tray] Tray registered successfully');
}

/**
 * 获取托盘管理器实例
 */
export function getTrayManager(): TrayManager | null {
  return trayManager;
}

/**
 * 销毁托盘
 */
export function destroyTray(): void {
  if (trayManager) {
    trayManager.destroy();
    trayManager = null;
  }
}

export { TrayManager } from './tray';
