/**
 * 提醒系统模块
 *
 * 提供三类独立提醒（运动、远眺、站立）的调度和窗口管理
 */

export { ReminderScheduler } from './scheduler';
export { Timeline } from './timeline';
export { ReminderWindowManager } from './reminder-window';
export type { ReminderType, ReminderState, SchedulerState, TriggerEvent } from './types';
