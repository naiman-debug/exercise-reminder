import Database from 'better-sqlite3';
import type { UserInfo, WeightRecord, Exercise, Activity, DailyStats, ReminderSettings } from './schema';

export class DatabaseQueries {
  private db: Database.Database;

  constructor(db: Database.Database) {
    this.db = db;
  }

  // ===== 用户信息 =====

  getUserInfo(): UserInfo | null {
    return this.db.prepare(`
      SELECT
        id, height, weight, age, gender,
        daily_target as dailyTarget,
        initial_weight as initialWeight,
        created_at as createdAt,
        updated_at as updatedAt
      FROM user_info
      WHERE id = 1
    `).get() as UserInfo | null;
  }

  saveUserInfo(info: Omit<UserInfo, 'id' | 'createdAt' | 'updatedAt'>) {
    const existing = this.getUserInfo();
    const now = new Date().toISOString();

    if (existing) {
      return this.db.prepare(`
        UPDATE user_info
        SET height = ?, weight = ?, age = ?, gender = ?, daily_target = ?, updated_at = ?
        WHERE id = 1
      `).run(info.height, info.weight, info.age, info.gender, info.dailyTarget, now);
    } else {
      return this.db.prepare(`
        INSERT INTO user_info (height, weight, age, gender, daily_target, initial_weight, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `).run(info.height, info.weight, info.age, info.gender, info.dailyTarget, info.weight, now, now);
    }
  }

  updateWeight(weight: number) {
    const now = new Date().toISOString();
    const date = new Date().toISOString().split('T')[0];

    // 更新当前体重
    this.db.prepare('UPDATE user_info SET weight = ?, updated_at = ? WHERE id = 1').run(weight, now);

    // 记录体重历史
    this.db.prepare(`
      INSERT OR IGNORE INTO weight_records (weight, record_date, created_at)
      VALUES (?, ?, ?)
    `).run(weight, date, now);

    // 更新今日体重的统计
    this.db.prepare('UPDATE daily_stats SET weight = ? WHERE date = ?').run(weight, date);
  }

  // ===== 运动库 =====

  getAllExercises(): Exercise[] {
    return this.db.prepare(`
      SELECT
        id, name,
        met_value as metValue,
        intensity,
        created_at as createdAt
      FROM exercises
      ORDER BY met_value DESC
    `).all() as Exercise[];
  }

  getExerciseByName(name: string): Exercise | null {
    return this.db.prepare(`
      SELECT
        id, name,
        met_value as metValue,
        intensity,
        created_at as createdAt
      FROM exercises
      WHERE name = ?
    `).get(name) as Exercise | null;
  }

  addExercise(name: string, metValue: number, intensity: string) {
    return this.db.prepare(`
      INSERT INTO exercises (name, met_value, intensity, created_at)
      VALUES (?, ?, ?, datetime('now'))
    `).run(name, metValue, intensity);
  }

  deleteExercise(id: number) {
    return this.db.prepare('DELETE FROM exercises WHERE id = ?').run(id);
  }

  // ===== 活动记录 =====

  saveActivity(activity: Omit<Activity, 'id'>) {
    const result = this.db.prepare(`
      INSERT INTO activities (type, name, duration, calories, met_value, weight, timestamp, date, completed)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      activity.type,
      activity.name,
      activity.duration,
      activity.calories || null,
      activity.metValue || null,
      activity.weight || null,
      activity.timestamp,
      activity.date,
      activity.completed ? 1 : 0
    );

    const statsRow = this.db.prepare(`
      SELECT
        SUM(CASE WHEN type = 'exercise' THEN calories ELSE 0 END) as total_calories,
        COUNT(CASE WHEN type = 'exercise' THEN 1 END) as exercise_count,
        COUNT(CASE WHEN type = 'gaze' THEN 1 END) as gaze_count,
        COUNT(CASE WHEN type = 'stand' THEN 1 END) as stand_count
      FROM activities
      WHERE date = ?
    `).get(activity.date) as { total_calories: number; exercise_count: number; gaze_count: number; stand_count: number };

    const user = this.getUserInfo();
    const targetCalories = user?.dailyTarget || 300;
    const totalCalories = statsRow?.total_calories || 0;
    const achieved = totalCalories >= targetCalories;

    this.saveDailyStats({
      id: 0,
      date: activity.date,
      totalCalories,
      targetCalories,
      achieved,
      achievedToday: achieved,
      exerciseCount: statsRow?.exercise_count || 0,
      gazeCount: statsRow?.gaze_count || 0,
      standCount: statsRow?.stand_count || 0,
      weight: activity.weight || user?.weight,
      streak: 0,
    });

    return result;
  }

  getActivitiesByDate(date: string): Activity[] {
    return this.db.prepare(`
      SELECT
        id, type, name, duration, calories,
        met_value as metValue,
        weight,
        timestamp, date,
        completed
      FROM activities
      WHERE date = ?
      ORDER BY timestamp DESC
    `).all(date) as Activity[];
  }

  getRecentActivities(limit: number = 50): Activity[] {
    return this.db.prepare(`
      SELECT
        id, type, name, duration, calories,
        met_value as metValue,
        weight,
        timestamp, date,
        completed
      FROM activities
      ORDER BY timestamp DESC
      LIMIT ?
    `).all(limit) as Activity[];
  }

  // ===== 统计数据 =====

  getTodayStats(date: string): DailyStats | null {
    const stats = this.db.prepare(`
      SELECT
        SUM(CASE WHEN type = 'exercise' THEN calories ELSE 0 END) as total_calories,
        COUNT(CASE WHEN type = 'exercise' THEN 1 END) as exercise_count,
        COUNT(CASE WHEN type = 'gaze' THEN 1 END) as gaze_count,
        COUNT(CASE WHEN type = 'stand' THEN 1 END) as stand_count
      FROM activities
      WHERE date = ?
    `).get(date) as { total_calories: number; exercise_count: number; gaze_count: number; stand_count: number };

    const user = this.getUserInfo();
    if (!stats || !user) return null;

    const targetCalories = user.dailyTarget;
    const achieved = (stats.total_calories >= targetCalories) ? 1 : 0;

    return {
      id: 0, // 临时 id，实际保存时会由数据库生成
      date,
      totalCalories: stats.total_calories || 0,
      targetCalories,
      achieved: achieved === 1,
      achievedToday: false,
      exerciseCount: stats.exercise_count || 0,
      gazeCount: stats.gaze_count || 0,
      standCount: stats.stand_count || 0,
      streak: 0,
    };
  }

  saveDailyStats(stats: DailyStats) {
    const existing = this.db.prepare('SELECT * FROM daily_stats WHERE date = ?').get(stats.date) as DailyStats | undefined;

    if (existing) {
      return this.db.prepare(`
        UPDATE daily_stats
        SET total_calories = ?, target_calories = ?, achieved = ?, achieved_today = ?, exercise_count = ?, gaze_count = ?, stand_count = ?, weight = ?, streak = ?
        WHERE date = ?
      `).run(
        stats.totalCalories,
        stats.targetCalories,
        stats.achieved ? 1 : 0,
        stats.achievedToday ? 1 : 0,
        stats.exerciseCount,
        stats.gazeCount,
        stats.standCount,
        stats.weight || null,
        stats.streak,
        stats.date
      );
    } else {
      return this.db.prepare(`
        INSERT INTO daily_stats (date, total_calories, target_calories, achieved, achieved_today, exercise_count, gaze_count, stand_count, weight, streak)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).run(
        stats.date,
        stats.totalCalories,
        stats.targetCalories,
        stats.achieved ? 1 : 0,
        stats.achievedToday ? 1 : 0,
        stats.exerciseCount,
        stats.gazeCount,
        stats.standCount,
        stats.weight || null,
        stats.streak
      );
    }
  }

  getStreakDays(): number {
    const today = new Date().toISOString().split('T')[0];
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];

    const todayStats = this.db.prepare('SELECT achieved FROM daily_stats WHERE date = ?').get(today) as { achieved: number } | undefined;
    const yesterdayStats = this.db.prepare('SELECT achieved FROM daily_stats WHERE date = ?').get(yesterday) as { achieved: number } | undefined;

    if (!todayStats) {
      // 今天还没有记录，从历史计算
      return this.calculateStreakFromHistory();
    }

    if (todayStats.achieved === 1 && yesterdayStats?.achieved === 1) {
      // 连续两天都打卡，继续往前算
      return 1 + this.getStreakDaysFrom(yesterday);
    } else if (todayStats.achieved === 1) {
      // 只有今天打卡
      return 1;
    } else {
      // 今天没打卡，重置
      return 0;
    }
  }

  private getStreakDaysFrom(date: string): number {
    const prevDate = new Date(Date.parse(date) - 86400000).toISOString().split('T')[0];
    const stats = this.db.prepare('SELECT achieved FROM daily_stats WHERE date = ?').get(prevDate) as { achieved: number } | undefined;

    if (!stats || stats.achieved !== 1) {
      return 0;
    }

    return 1 + this.getStreakDaysFrom(prevDate);
  }

  private calculateStreakFromHistory(): number {
    // 从最近的记录开始计算
    const result = this.db.prepare(`
      SELECT date, achieved FROM daily_stats
      ORDER BY date DESC
    `).get() as { date: string; achieved: number } | undefined;

    if (!result || !result.achieved) {
      return 0;
    }

    return 1 + this.getStreakDaysFrom(result.date);
  }

  // ===== 提醒设置 =====

  getReminderSettings(): ReminderSettings[] {
    return this.db.prepare(`
      SELECT
        id,
        type,
        interval_min as intervalMin,
        interval_max as intervalMax,
        duration,
        enabled,
        updated_at as updatedAt
      FROM reminder_settings
    `).all() as ReminderSettings[];
  }

  getReminderSetting(type: 'exercise' | 'gaze' | 'stand'): ReminderSettings | null {
    return this.db.prepare(`
      SELECT
        id,
        type,
        interval_min as intervalMin,
        interval_max as intervalMax,
        duration,
        enabled,
        updated_at as updatedAt
      FROM reminder_settings
      WHERE type = ?
    `).get(type) as ReminderSettings | null;
  }

  updateReminderSettings(type: 'exercise' | 'gaze' | 'stand', settings: Omit<ReminderSettings, 'id' | 'updatedAt'>) {
    return this.db.prepare(`
      UPDATE reminder_settings
      SET interval_min = ?, interval_max = ?, duration = ?, enabled = ?, updated_at = datetime('now')
      WHERE type = ?
    `).run(settings.intervalMin, settings.intervalMax, settings.duration, settings.enabled ? 1 : 0, type);
  }

  // ===== 系统设置 =====

  getSystemSetting(key: string): string | null {
    const result = this.db.prepare('SELECT value FROM system_settings WHERE key = ?').get(key) as { value: string } | undefined;
    return result?.value || null;
  }

  setSystemSetting(key: string, value: string) {
    return this.db.prepare(`
      INSERT OR REPLACE INTO system_settings (key, value, updated_at)
      VALUES (?, ?, datetime('now'))
    `).run(key, value);
  }
}
