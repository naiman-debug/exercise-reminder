// 前端常量定义

export const REMINDER_TYPES = {
  EXERCISE: 'exercise',
  GAZE: 'gaze',
  STAND: 'stand',
} as const;

export const INTENSITY_LEVELS = {
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low',
} as const;

export const GENDER = {
  MALE: 'male',
  FEMALE: 'female',
} as const;

// 默认值
export const DEFAULTS = {
  HEIGHT: 170, // cm
  WEIGHT: 65, // kg
  AGE: 30,
  DAILY_TARGET: 300, // 大卡

  // 提醒设置
  EXERCISE_INTERVAL_MIN: 10, // 分钟
  EXERCISE_INTERVAL_MAX: 20, // 分钟
  EXERCISE_DURATION: 120, // 秒

  GAZE_INTERVAL_MIN: 10, // 分钟
  GAZE_INTERVAL_MAX: 20, // 分钟
  GAZE_DURATION: 60, // 秒

  STAND_INTERVAL_MIN: 10, // 分钟
  STAND_INTERVAL_MAX: 20, // 分钟
  STAND_DURATION: 300, // 秒
} as const;

// 颜色主题
export const COLORS = {
  PRIMARY: '#7C3AED',
  PRIMARY_LIGHT: '#A855F7',
  SUCCESS: '#10B981',
  WARNING: '#F59E0B',
  ERROR: '#EF4444',
  INFO: '#3B82F6',

  // 强度标签颜色
  HIGH_INTENSITY: '#EF4444',
  MEDIUM_INTENSITY: '#F59E0B',
  LOW_INTENSITY: '#10B981',
} as const;
