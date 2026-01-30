import { contextBridge, ipcRenderer, IpcRendererEvent } from 'electron';
import { IPC_CHANNELS } from './ipc/channels';

// API 类型定义
export interface ElectronAPI {
  // 用户相关
  getUserInfo: () => Promise<any>;
  saveUserInfo: (info: any) => Promise<any>;
  updateWeight: (weight: number) => Promise<{ success: boolean }>;

  // 运动库
  getAllExercises: () => Promise<any[]>;
  getExerciseByName: (name: string) => Promise<any>;
  addExercise: (exercise: any) => Promise<any>;
  deleteExercise: (id: number) => Promise<any>;

  // 活动记录
  saveActivity: (activity: any) => Promise<any>;
  getActivitiesByDate: (date: string) => Promise<any[]>;
  getRecentActivities: (limit?: number) => Promise<any[]>;

  // 统计数据
  getTodayStats: (date: string) => Promise<any>;
  getHistoryStats: () => Promise<any>;
  getStreakDays: () => Promise<number>;

  // 提醒设置
  getReminderSettings: () => Promise<any[]>;
  getReminderSetting: (type: 'exercise' | 'gaze' | 'stand') => Promise<any>;
  updateReminderSettings: (settings: any) => Promise<any>;

  // 提醒控制
  pauseReminders: () => Promise<{ success: boolean }>;
  resumeReminders: () => Promise<{ success: boolean }>;
  getReminderStatus: () => Promise<{ isRunning: boolean; isPaused: boolean }>;

  // 系统功能
  getSystemSetting: (key: string) => Promise<string | null>;
  setSystemSetting: (key: string, value: string) => Promise<any>;

  // 窗口控制
  showMainWindow: () => Promise<{ success: boolean }>;
  showSettingsWindow: () => Promise<{ success: boolean }>;
  showReminder: (type: 'exercise' | 'gaze' | 'stand') => Promise<{ success: boolean }>;
  closeReminder: () => Promise<{ success: boolean }>;

  // 事件监听
  onReminderTrigger: (callback: (event: any) => void) => () => void;
  removeAllListeners: (channel: string) => void;
}

// 暴露 API 到渲染进程
const electronAPI: ElectronAPI = {
  // 用户相关
  getUserInfo: () => ipcRenderer.invoke(IPC_CHANNELS.GET_USER_INFO),
  saveUserInfo: (info) => ipcRenderer.invoke(IPC_CHANNELS.SAVE_USER_INFO, info),
  updateWeight: (weight) => ipcRenderer.invoke(IPC_CHANNELS.UPDATE_WEIGHT, weight),

  // 运动库
  getAllExercises: () => ipcRenderer.invoke(IPC_CHANNELS.GET_ALL_EXERCISES),
  getExerciseByName: (name) => ipcRenderer.invoke(IPC_CHANNELS.GET_EXERCISE_BY_NAME, name),
  addExercise: (exercise) => ipcRenderer.invoke(IPC_CHANNELS.ADD_EXERCISE, exercise),
  deleteExercise: (id) => ipcRenderer.invoke(IPC_CHANNELS.DELETE_EXERCISE, id),

  // 活动记录
  saveActivity: (activity) => ipcRenderer.invoke(IPC_CHANNELS.SAVE_ACTIVITY, activity),
  getActivitiesByDate: (date) => ipcRenderer.invoke(IPC_CHANNELS.GET_ACTIVITIES_BY_DATE, date),
  getRecentActivities: (limit) => ipcRenderer.invoke(IPC_CHANNELS.GET_RECENT_ACTIVITIES, limit),

  // 统计数据
  getTodayStats: (date) => ipcRenderer.invoke(IPC_CHANNELS.GET_TODAY_STATS, date),
  getHistoryStats: () => ipcRenderer.invoke(IPC_CHANNELS.GET_HISTORY_STATS),
  getStreakDays: () => ipcRenderer.invoke(IPC_CHANNELS.GET_STREAK_DAYS),

  // 提醒设置
  getReminderSettings: () => ipcRenderer.invoke(IPC_CHANNELS.GET_REMINDER_SETTINGS),
  getReminderSetting: (type) => ipcRenderer.invoke(IPC_CHANNELS.GET_REMINDER_SETTING, type),
  updateReminderSettings: (settings) => ipcRenderer.invoke(IPC_CHANNELS.UPDATE_REMINDER_SETTINGS, settings),

  // 提醒控制
  pauseReminders: () => ipcRenderer.invoke(IPC_CHANNELS.PAUSE_REMINDERS),
  resumeReminders: () => ipcRenderer.invoke(IPC_CHANNELS.RESUME_REMINDERS),
  getReminderStatus: () => ipcRenderer.invoke(IPC_CHANNELS.GET_REMINDER_STATUS),

  // 系统功能
  getSystemSetting: (key) => ipcRenderer.invoke(IPC_CHANNELS.GET_SYSTEM_SETTING, key),
  setSystemSetting: (key, value) => ipcRenderer.invoke(IPC_CHANNELS.SET_SYSTEM_SETTING, key, value),

  // 窗口控制
  showMainWindow: () => ipcRenderer.invoke(IPC_CHANNELS.SHOW_MAIN_WINDOW),
  showSettingsWindow: () => ipcRenderer.invoke(IPC_CHANNELS.SHOW_SETTINGS_WINDOW),
  showReminder: (type) => ipcRenderer.invoke(IPC_CHANNELS.SHOW_REMINDER, type),
  closeReminder: () => ipcRenderer.invoke(IPC_CHANNELS.CLOSE_REMINDER),

  // 事件监听
  onReminderTrigger: (callback) => {
    const listener = (_event: IpcRendererEvent, data: any) => callback(data);
    ipcRenderer.on('reminder:trigger', listener);
    return () => ipcRenderer.removeListener('reminder:trigger', listener);
  },

  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),
};

// 使用 contextBridge 安全暴露 API
contextBridge.exposeInMainWorld('electronAPI', electronAPI);

// TypeScript 类型声明（供渲染进程使用）
declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
