/**
 * Zod 验证 Schema
 * 用于用户输入验证和数据校验
 */

import { z } from 'zod';

// ===== 用户信息验证 =====

export const UserInfoSchema = z.object({
  height: z.number()
    .min(100, '身高不能小于 100cm')
    .max(250, '身高不能大于 250cm'),
  weight: z.number()
    .min(30, '体重不能小于 30kg')
    .max(300, '体重不能大于 300kg'),
  age: z.number()
    .min(10, '年龄不能小于 10 岁')
    .max(120, '年龄不能大于 120 岁'),
  gender: z.enum(['male', 'female']),
  dailyTarget: z.number()
    .min(50, '每日目标不能小于 50 大卡')
    .max(2000, '每日目标不能大于 2000 大卡'),
  initialWeight: z.number()
    .min(30, '初始体重不能小于 30kg')
    .max(300, '初始体重不能大于 300kg'),
});

export type UserInfoInput = z.infer<typeof UserInfoSchema>;

// ===== 运动验证 =====

export const ExerciseSchema = z.object({
  name: z.string()
    .min(1, '运动名称不能为空')
    .max(50, '运动名称不能超过 50 个字符')
    .regex(/^[\u4e00-\u9fa5a-zA-Z0-9\s]+$/, '运动名称只能包含中文、英文、数字和空格'),
  metValue: z.number()
    .min(1, 'MET 值必须大于 0')
    .max(20, 'MET 值不能大于 20'),
  intensity: z.enum(['low', 'medium', 'high']),
});

export type ExerciseInput = z.infer<typeof ExerciseSchema>;

// ===== 活动记录验证 =====

export const ActivitySchema = z.object({
  type: z.enum(['exercise', 'gaze', 'stand']),
  name: z.string().min(1, '活动名称不能为空').max(100, '活动名称不能超过 100 个字符'),
  duration: z.number()
    .min(1, '持续时间必须大于 0 秒')
    .max(3600, '持续时间不能超过 1 小时'),
  calories: z.number()
    .min(0, '消耗热量不能为负数')
    .max(5000, '消耗热量不能大于 5000 大卡')
    .optional(),
  metValue: z.number()
    .min(0, 'MET 值不能为负数')
    .optional(),
  weight: z.number()
    .min(30, '体重不能小于 30kg')
    .max(300, '体重不能大于 300kg')
    .optional(),
  timestamp: z.string().datetime({ message: '时间戳格式错误' }),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, { message: '日期格式必须是 YYYY-MM-DD' }),
  completed: z.boolean(),
});

export type ActivityInput = z.infer<typeof ActivitySchema>;

// ===== 提醒设置验证 =====

export const ReminderSettingsSchema = z.object({
  type: z.enum(['exercise', 'gaze', 'stand']),
  intervalMin: z.number()
    .min(1, '间隔时间不能小于 1 分钟')
    .max(120, '间隔时间不能超过 120 分钟'),
  intervalMax: z.number()
    .min(1, '间隔时间不能小于 1 分钟')
    .max(120, '间隔时间不能超过 120 分钟'),
  duration: z.number()
    .min(10, '持续时间不能小于 10 秒')
    .max(600, '持续时间不能超过 10 分钟'),
  enabled: z.boolean(),
});

export type ReminderSettingsInput = z.infer<typeof ReminderSettingsSchema>;

// ===== 验证辅助函数 =====

/**
 * 验证用户信息
 */
export function validateUserInfo(data: unknown): { success: boolean; data?: UserInfoInput; errors?: string[] } {
  const result = UserInfoSchema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const errors = result.error.issues.map(issue => `${issue.path.join('.')}: ${issue.message}`);
  return { success: false, errors };
}

/**
 * 验证运动数据
 */
export function validateExercise(data: unknown): { success: boolean; data?: ExerciseInput; errors?: string[] } {
  const result = ExerciseSchema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const errors = result.error.issues.map(issue => `${issue.path.join('.')}: ${issue.message}`);
  return { success: false, errors };
}

/**
 * 验证提醒设置
 */
export function validateReminderSettings(data: unknown): { success: boolean; data?: ReminderSettingsInput; errors?: string[] } {
  const result = ReminderSettingsSchema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const errors = result.error.issues.map(issue => `${issue.path.join('.')}: ${issue.message}`);
  return { success: false, errors };
}

/**
 * 验证活动记录
 */
export function validateActivity(data: unknown): { success: boolean; data?: ActivityInput; errors?: string[] } {
  const result = ActivitySchema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const errors = result.error.issues.map(issue => `${issue.path.join('.')}: ${issue.message}`);
  return { success: false, errors };
}
