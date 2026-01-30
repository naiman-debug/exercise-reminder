import { ipcMain, BrowserWindow } from 'electron';
import { IPC_CHANNELS } from './channels';
import { getDatabase } from '../database/db';
import { DatabaseQueries } from '../database/queries';

export function registerIPCHandlers() {
  const db = getDatabase();
  const queries = new DatabaseQueries(db);

  // ===== 用户相关 =====

  ipcMain.handle(IPC_CHANNELS.GET_USER_INFO, () => {
    return queries.getUserInfo();
  });

  ipcMain.handle(IPC_CHANNELS.SAVE_USER_INFO, (_, userInfo) => {
    return queries.saveUserInfo(userInfo);
  });

  ipcMain.handle(IPC_CHANNELS.UPDATE_WEIGHT, (_, weight: number) => {
    queries.updateWeight(weight);
    return { success: true };
  });

  // ===== 运动库 =====

  ipcMain.handle(IPC_CHANNELS.GET_ALL_EXERCISES, () => {
    return queries.getAllExercises();
  });

  ipcMain.handle(IPC_CHANNELS.GET_EXERCISE_BY_NAME, (_, name: string) => {
    return queries.getExerciseByName(name);
  });

  ipcMain.handle(IPC_CHANNELS.ADD_EXERCISE, (_, exercise) => {
    return queries.addExercise(exercise.name, exercise.metValue, exercise.intensity);
  });

  ipcMain.handle(IPC_CHANNELS.DELETE_EXERCISE, (_, id: number) => {
    return queries.deleteExercise(id);
  });

  // ===== 活动记录 =====

  ipcMain.handle(IPC_CHANNELS.SAVE_ACTIVITY, (_, activity) => {
    const result = queries.saveActivity(activity);

    // 检查是否达成每日目标
    const today = new Date().toISOString().split('T')[0];
    const stats = queries.getTodayStats(today);

    if (stats && stats.totalCalories >= stats.targetCalories && !stats.achievedToday) {
      stats.achievedToday = 1;
      queries.saveDailyStats(stats);

      // 显示目标完成庆祝弹窗
      showGoalAchievedNotification(stats.totalCalories, stats.targetCalories);
    }

    return result;
  });

  ipcMain.handle(IPC_CHANNELS.GET_ACTIVITIES_BY_DATE, (_, date: string) => {
    return queries.getActivitiesByDate(date);
  });

  ipcMain.handle(IPC_CHANNELS.GET_RECENT_ACTIVITIES, (_, limit = 50) => {
    return queries.getRecentActivities(limit);
  });

  // ===== 统计数据 =====

  ipcMain.handle(IPC_CHANNELS.GET_TODAY_STATS, (_, date: string) => {
    const stats = queries.getTodayStats(date);

    if (stats && !stats.weight) {
      const user = queries.getUserInfo();
      if (user) {
        stats.weight = user.weight;
      }
    }

    return stats;
  });

  ipcMain.handle(IPC_CHANNELS.GET_HISTORY_STATS, () => {
    const user = queries.getUserInfo();
    if (!user) return null;

    const totalResult = this.db.prepare(`
      SELECT SUM(total_calories) as total_calories
      FROM daily_stats
    `).get() as { total_calories: number } | undefined;

    const exerciseCount = this.db.prepare(`
      SELECT COUNT(*) as count
      FROM daily_stats
      WHERE achieved = 1
    `).get() as { count: number } | undefined;

    return {
      totalCalories: totalResult?.total_calories || 0,
      totalStreak: queries.getStreakDays(),
      weightChange: {
        initial: user.initialWeight,
        current: user.weight,
        delta: user.weight - user.initialWeight,
      },
      totalAchieved: exerciseCount?.count || 0,
    };
  });

  ipcMain.handle(IPC_CHANNELS.GET_STREAK_DAYS, () => {
    return queries.getStreakDays();
  });

  // ===== 提醒设置 =====

  ipcMain.handle(IPC_CHANNELS.GET_REMINDER_SETTINGS, () => {
    return queries.getReminderSettings();
  });

  ipcMain.handle(IPC_CHANNELS.GET_REMINDER_SETTING, (_, type: 'exercise' | 'gaze' | 'stand') => {
    return queries.getReminderSetting(type);
  });

  ipcMain.handle(IPC_CHANNELS.UPDATE_REMINDER_SETTINGS, (_, settings) => {
    return queries.updateReminderSettings(settings.type, settings);
  });

  // ===== 提醒控制 =====

  let isPaused = false;

  ipcMain.handle(IPC_CHANNELS.PAUSE_REMINDERS, () => {
    isPaused = true;
    return { success: true };
  });

  ipcMain.handle(IPC_CHANNELS.RESUME_REMINDERS, () => {
    isPaused = false;
    return { success: true };
  });

  ipcMain.handle(IPC_CHANNELS.GET_REMINDER_STATUS, () => {
    return { isPaused };
  });

  // ===== 系统功能 =====

  ipcMain.handle(IPC_CHANNELS.GET_SYSTEM_SETTING, (_, key: string) => {
    return queries.getSystemSetting(key);
  });

  ipcMain.handle(IPC_CHANNELS.SET_SYSTEM_SETTING, (_, key: string, value: string) => {
    return queries.setSystemSetting(key, value);
  });

  // ===== 窗口控制 =====

  ipcMain.handle(IPC_CHANNELS.SHOW_MAIN_WINDOW, () => {
    const mainWindow = BrowserWindow.getAllWindows()[0];
    if (mainWindow) {
      if (mainWindow.isMinimized()) {
        mainWindow.restore();
      }
      mainWindow.show();
      mainWindow.focus();
    }
    return { success: true };
  });

  ipcMain.handle(IPC_CHANNELS.SHOW_SETTINGS_WINDOW, () => {
    // TODO: 实现设置窗口
    return { success: true };
  });

  ipcMain.handle(IPC_CHANNELS.SHOW_REMINDER, (_, type: 'exercise' | 'gaze' | 'stand') => {
    // TODO: 实现提醒窗口
    return { success: true };
  });

  ipcMain.handle(IPC_CHANNELS.CLOSE_REMINDER, () => {
    // TODO: 关闭提醒窗口
    return { success: true };
  });
}

// 显示目标完成庆祝弹窗
function showGoalAchievedNotification(achieved: number, target: number) {
  const celebration = new BrowserWindow({
    width: 400,
    height: 250,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    resizable: false,
    movable: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: require('path').join(__dirname, '../dist-electron/preload.js'),
    },
  });

  const center = celebration.getBounds();
  const display = require('electron').screen.getPrimaryDisplay();
  const x = Math.floor((display.workAreaSize.width - center.width) / 2);
  const y = Math.floor((display.workAreaSize.height - center.height) / 2);
  celebration.setPosition(x, y);

  const params = new URLSearchParams({
    achieved: achieved.toString(),
    target: target.toString(),
  });

  if (process.env.NODE_ENV === 'development') {
    celebration.loadURL(`http://localhost:5173/#/celebration?${params.toString()}`);
  } else {
    celebration.loadURL(`file://${path.join(__dirname, '../dist-renderer/index.html')}#/celebration?${params.toString()}`);
  }

  // 3秒后自动关闭
  setTimeout(() => {
    if (!celebration.isDestroyed()) {
      celebration.close();
    }
  }, 3000);
}
