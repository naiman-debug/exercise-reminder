import { ReminderType } from './types';

/**
 * 单个提醒时间线
 * 管理单个提醒类型的调度逻辑
 */
export class Timeline {
  private timer: NodeJS.Timeout | null = null;
  private nextTriggerTime: number = 0;

  constructor(
    private type: ReminderType,
    private intervalMin: number,
    private intervalMax: number,
    private duration: number,
    private onTrigger: (type: ReminderType) => void
  ) {}

  /**
   * 计算下次触发时间
   * @param earliestTime 最早触发时间（Unix timestamp）
   */
  schedule(earliestTime: number): number {
    // 清除现有定时器
    if (this.timer) {
      clearTimeout(this.timer);
    }

    // 计算随机延迟（秒）
    const minDelay = this.intervalMin * 60;
    const maxDelay = this.intervalMax * 60;
    const delay = Math.floor(
      Math.random() * (maxDelay - minDelay + 1) + minDelay
    );

    // 计算下次触发时间（Unix timestamp，毫秒）
    const now = Date.now();
    this.nextTriggerTime = Math.max(now + delay * 1000, earliestTime);

    // 设置定时器
    const delayMs = this.nextTriggerTime - now;
    this.timer = setTimeout(() => {
      this.onTrigger(this.type);
    }, delayMs);

    return this.nextTriggerTime;
  }

  /**
   * 暂停时间线
   */
  pause(): void {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
  }

  /**
   * 获取下次触发时间
   */
  getNextTriggerTime(): number {
    return this.nextTriggerTime;
  }

  /**
   * 更新间隔参数
   */
  updateParams(intervalMin: number, intervalMax: number, duration: number): void {
    this.intervalMin = intervalMin;
    this.intervalMax = intervalMax;
    this.duration = duration;
  }

  /**
   * 销毁时间线
   */
  destroy(): void {
    this.pause();
  }
}
