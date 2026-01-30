/// <reference types="vite/client" />

// API 类型定义（从 preload 复制，避免循环依赖）
interface ElectronAPI {
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

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}

export {};
