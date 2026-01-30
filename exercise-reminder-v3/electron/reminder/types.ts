/** 提醒类型 */
export type ReminderType = 'exercise' | 'gaze' | 'stand';

/** 提醒状态 */
export interface ReminderState {
  type: ReminderType;
  isScheduled: boolean;
  nextTriggerTime: number; // Unix timestamp
  intervalMin: number;
  intervalMax: number;
  duration: number;
}

/** 调度器状态 */
export interface SchedulerState {
  isRunning: boolean;
  isPaused: boolean;
  reminders: {
    exercise: ReminderState;
    gaze: ReminderState;
    stand: ReminderState;
  };
}

/** 触发事件 */
export interface TriggerEvent {
  type: ReminderType;
  timestamp: number;
  exerciseName?: string;
  metValue?: number;
  duration: number;
}
