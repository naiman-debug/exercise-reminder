// 前端类型定义

export interface UserInfo {
  id: number;
  height: number;
  weight: number;
  age: number;
  gender: 'male' | 'female';
  dailyTarget: number;
  initialWeight: number;
  createdAt: string;
  updatedAt: string;
}

export interface WeightRecord {
  id: number;
  weight: number;
  recordDate: string;
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
  duration: number;
  calories?: number;
  metValue?: number;
  weight?: number;
  timestamp: string;
  date: string;
  completed: boolean;
}

export interface DailyStats {
  id?: number;
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
  id?: number;
  type: 'exercise' | 'gaze' | 'stand';
  intervalMin: number;
  intervalMax: number;
  duration: number;
  enabled: boolean;
  updatedAt?: string;
}

export interface ReminderStatus {
  isRunning: boolean;
  isPaused: boolean;
}

export interface HistoryStats {
  totalCalories: number;
  totalStreak: number;
  weightChange: {
    initial: number;
    current: number;
    delta: number;
  };
  totalAchieved: number;
}

export interface TriggerEventData {
  type: 'exercise' | 'gaze' | 'stand';
  timestamp: number;
  exerciseName?: string;
  metValue?: number;
  duration: number;
}
