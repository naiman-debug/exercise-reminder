// IPC 通道常量定义

export const IPC_CHANNELS = {
  // ===== 用户相关 =====
  GET_USER_INFO: 'get-user-info',
  SAVE_USER_INFO: 'save-user-info',
  UPDATE_WEIGHT: 'update-weight',

  // ===== 运动库 =====
  GET_ALL_EXERCISES: 'get-all-exercises',
  GET_EXERCISE_BY_NAME: 'get-exercise-by-name',
  ADD_EXERCISE: 'add-exercise',
  DELETE_EXERCISE: 'delete-exercise',

  // ===== 活动记录 =====
  SAVE_ACTIVITY: 'save-activity',
  GET_ACTIVITIES_BY_DATE: 'get-activities-by-date',
  GET_RECENT_ACTIVITIES: 'get-recent-activities',

  // ===== 统计数据 =====
  GET_TODAY_STATS: 'get-today-stats',
  GET_HISTORY_STATS: 'get-history-stats',
  GET_STREAK_DAYS: 'get-streak-days',

  // ===== 提醒设置 =====
  GET_REMINDER_SETTINGS: 'get-reminder-settings',
  GET_REMINDER_SETTING: 'get-reminder-setting',
  UPDATE_REMINDER_SETTINGS: 'update-reminder-settings',

  // ===== 提醒控制 =====
  PAUSE_REMINDERS: 'pause-reminders',
  RESUME_REMINDERS: 'resume-reminders',
  GET_REMINDER_STATUS: 'get-reminder-status',

  // ===== 系统功能 =====
  GET_SYSTEM_SETTING: 'get-system-setting',
  SET_SYSTEM_SETTING: 'set-system-setting',
  GET_AUTO_START: 'get-auto-start',
  SET_AUTO_START: 'set-auto-start',
  GET_GLOBAL_MIN_INTERVAL: 'get-global-min-interval',
  SET_GLOBAL_MIN_INTERVAL: 'set-global-min-interval',

  // ===== 窗口控制 =====
  SHOW_MAIN_WINDOW: 'show-main-window',
  SHOW_SETTINGS_WINDOW: 'show-settings-window',
  SHOW_REMINDER: 'show-reminder',
  CLOSE_REMINDER: 'close-reminder',
} as const;
