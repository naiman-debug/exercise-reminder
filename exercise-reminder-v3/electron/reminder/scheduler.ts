import { BrowserWindow } from 'electron';
import { DatabaseQueries } from '../database/queries';
import { Timeline } from './timeline';
import { ReminderWindowManager } from './reminder-window';
import { ReminderType, SchedulerState, TriggerEvent } from './types';

/**
 * 提醒系统调度器
 * 管理三类提醒的独立调度，确保全局最小间隔
 */
export class ReminderScheduler {
  private timelines: Map<ReminderType, Timeline> = new Map();
  private windowManager: ReminderWindowManager;
  private globalMinIntervalMs = 300 * 1000;
  private lastTriggerTime = 0;
  private state: SchedulerState = {
    isRunning: false,
    isPaused: false,
    reminders: {
      exercise: {
        type: 'exercise',
        isScheduled: false,
        nextTriggerTime: 0,
        intervalMin: 10,
        intervalMax: 20,
        duration: 120
      },
      gaze: {
        type: 'gaze',
        isScheduled: false,
        nextTriggerTime: 0,
        intervalMin: 10,
        intervalMax: 20,
        duration: 60
      },
      stand: {
        type: 'stand',
        isScheduled: false,
        nextTriggerTime: 0,
        intervalMin: 10,
        intervalMax: 20,
        duration: 300
      }
    }
  };

  constructor(
    private queries: DatabaseQueries,
    private getWindow: () => BrowserWindow | null
  ) {
    this.windowManager = new ReminderWindowManager();
  }

  /**
   * 启动调度器
   */
  async start(): Promise<void> {
    if (this.state.isRunning) {
      console.log('[ReminderScheduler] Already running');
      return;
    }

    console.log('[ReminderScheduler] Starting...');

    const settings = this.queries.getReminderSettings();
    settings.forEach(setting => {
      const reminder = this.state.reminders[setting.type];
      if (reminder) {
        reminder.intervalMin = setting.intervalMin;
        reminder.intervalMax = setting.intervalMax;
        reminder.duration = setting.duration;
        console.log(`[ReminderScheduler] Loaded ${setting.type} settings: ${setting.intervalMin}-${setting.intervalMax}min, ${setting.duration}s`);
      }
    });

    const globalIntervalSetting = this.queries.getSystemSetting('global_min_interval_sec');
    if (globalIntervalSetting) {
      const parsed = Number(globalIntervalSetting);
      if (!Number.isNaN(parsed) && parsed >= 0) {
        this.globalMinIntervalMs = parsed * 1000;
      }
    } else {
      this.queries.setSystemSetting('global_min_interval_sec', String(this.globalMinIntervalMs / 1000));
    }

    this.timelines.set('exercise', new Timeline(
      'exercise',
      this.state.reminders.exercise.intervalMin,
      this.state.reminders.exercise.intervalMax,
      this.state.reminders.exercise.duration,
      (type) => this.handleTrigger(type)
    ));

    this.timelines.set('gaze', new Timeline(
      'gaze',
      this.state.reminders.gaze.intervalMin,
      this.state.reminders.gaze.intervalMax,
      this.state.reminders.gaze.duration,
      (type) => this.handleTrigger(type)
    ));

    this.timelines.set('stand', new Timeline(
      'stand',
      this.state.reminders.stand.intervalMin,
      this.state.reminders.stand.intervalMax,
      this.state.reminders.stand.duration,
      (type) => this.handleTrigger(type)
    ));

    const now = Date.now();
    this.timelines.forEach((timeline, type) => {
      const nextTime = timeline.schedule(now);
      console.log(`[ReminderScheduler] ${type} next trigger: ${new Date(nextTime).toLocaleString()}`);
    });

    this.state.isRunning = true;
    console.log('[ReminderScheduler] Started successfully');
  }

  /**
   * 处理提醒触发
   */
  private async handleTrigger(type: ReminderType): Promise<void> {
    console.log(`[ReminderScheduler] Triggered: ${type}`);

    if (this.state.isPaused) {
      console.log('[ReminderScheduler] Paused, skipping trigger');
      return;
    }

    const user = this.queries.getUserInfo();
    if (!user) {
      console.log('[ReminderScheduler] No user info found, skipping trigger');
      return;
    }

    let eventData: TriggerEvent = {
      type,
      timestamp: Date.now(),
      duration: this.state.reminders[type].duration
    };

    if (type === 'exercise') {
      const exercises = this.queries.getAllExercises();
      if (exercises.length === 0) {
        console.log('[ReminderScheduler] No exercises found, skipping trigger');
        return;
      }
      const randomExercise = exercises[Math.floor(Math.random() * exercises.length)];
      eventData.exerciseName = randomExercise.name;
      eventData.metValue = randomExercise.metValue;
      console.log(`[ReminderScheduler] Selected exercise: ${randomExercise.name} (MET: ${randomExercise.metValue})`);
    }

    this.windowManager.showReminder(eventData);

    this.lastTriggerTime = Date.now();
    const earliestTime = this.lastTriggerTime + this.globalMinIntervalMs;
    this.timelines.forEach((timeline, reminderType) => {
      const nextTime = timeline.schedule(earliestTime);
      console.log(`[ReminderScheduler] ${reminderType} rescheduled, next trigger: ${new Date(nextTime).toLocaleString()}`);
    });
  }

  /**
   * 暂停调度器
   */
  pause(): void {
    this.state.isPaused = true;
    console.log('[ReminderScheduler] Paused');
  }

  /**
   * 恢复调度器
   */
  resume(): void {
    this.state.isPaused = false;
    console.log('[ReminderScheduler] Resumed');
  }

  /**
   * 更新提醒设置
   */
  updateReminderSettings(
    type: ReminderType,
    intervalMin: number,
    intervalMax: number,
    duration: number
  ): void {
    console.log(`[ReminderScheduler] Updating ${type} settings: ${intervalMin}-${intervalMax}min, ${duration}s`);

    const reminder = this.state.reminders[type];
    if (reminder) {
      reminder.intervalMin = intervalMin;
      reminder.intervalMax = intervalMax;
      reminder.duration = duration;
    }

    const timeline = this.timelines.get(type);
    if (timeline) {
      timeline.updateParams(intervalMin, intervalMax, duration);
      const nextTime = timeline.schedule(Date.now());
      console.log(`[ReminderScheduler] ${type} rescheduled with new params: ${new Date(nextTime).toLocaleString()}`);
    }
  }

  /**
   * 更新全局最小间隔
   */
  updateGlobalMinInterval(seconds: number): void {
    const safeSeconds = Math.max(0, Math.floor(seconds));
    this.globalMinIntervalMs = safeSeconds * 1000;
    const earliestTime = Math.max(Date.now(), this.lastTriggerTime + this.globalMinIntervalMs);
    this.timelines.forEach((timeline, reminderType) => {
      const nextTime = timeline.schedule(earliestTime);
      console.log(`[ReminderScheduler] ${reminderType} rescheduled with global min interval: ${new Date(nextTime).toLocaleString()}`);
    });
  }

  /**
   * 获取调度器状态
   */
  getState(): SchedulerState {
    return { ...this.state };
  }

  /**
   * 获取窗口管理器
   */
  getWindowManager(): ReminderWindowManager {
    return this.windowManager;
  }

  /**
   * 停止调度器
   */
  stop(): void {
    console.log('[ReminderScheduler] Stopping...');

    this.timelines.forEach((timeline) => timeline.destroy());
    this.timelines.clear();
    this.windowManager.closeReminder();

    this.state.isRunning = false;
    this.state.isPaused = false;

    console.log('[ReminderScheduler] Stopped');
  }
}
