// 数据库表类型定义

export interface UserInfo {
  id: number;
  height: number;        // cm
  weight: number;        // kg
  age: number;
  gender: 'male' | 'female';
  dailyTarget: number;   // 大卡
  initialWeight: number;
  createdAt: string;
  updatedAt: string;
}

export interface WeightRecord {
  id: number;
  weight: number;        // kg
  recordDate: string;    // YYYY-MM-DD
  createdAt: string;
}

export interface Exercise {
  id: number;
  name: string;
  metValue: number;
  intensity: 'high' | 'medium' | 'low';
  createdAt: string;
}

export interface Activity {
  id: number;
  type: 'exercise' | 'gaze' | 'stand';
  name: string;
  duration: number;      // 秒
  calories?: number;     // 大卡（仅运动）
  metValue?: number;
  weight?: number;
  timestamp: string;
  date: string;          // YYYY-MM-DD
  completed: boolean;
}

export interface DailyStats {
  id: number;
  date: string;
  totalCalories: number;
  targetCalories: number;
  achieved: boolean;
  achievedToday: boolean;
  exerciseCount: number;
  gazeCount: number;
  standCount: number;
  weight?: number;
  streak: number;
}

export interface ReminderSettings {
  id: number;
  type: 'exercise' | 'gaze' | 'stand';
  intervalMin: number;
  intervalMax: number;
  duration: number;
  enabled: boolean;
  updatedAt: string;
}

export interface SystemSetting {
  key: string;
  value: string;
  updatedAt: string;
}
