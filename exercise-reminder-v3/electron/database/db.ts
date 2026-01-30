import Database from 'better-sqlite3';
import path from 'path';
import { app } from 'electron';

const DB_NAME = 'health-reminder.db';

let dbInstance: Database.Database | null = null;

export function getDatabase(): Database.Database {
  if (!dbInstance) {
    const userDataPath = app.getPath('userData');
    const dbPath = path.join(userDataPath, DB_NAME);

    dbInstance = new Database(dbPath);

    // 启用 WAL 模式，提高并发性能
    dbInstance.pragma('journal_mode = WAL');
    dbInstance.pragma('foreign_keys = ON');

    // 初始化数据库表
    initDatabase(dbInstance);

    console.log('数据库连接成功:', dbPath);
  }

  return dbInstance;
}

function initDatabase(db: Database.Database) {
  // 创建所有表
  createTables(db);

  // 初始化数据
  initData(db);
}

function createTables(db: Database.Database) {
  // 用户信息表
  db.exec(`
    CREATE TABLE IF NOT EXISTS user_info (
      id INTEGER PRIMARY KEY,
      height REAL NOT NULL,
      weight REAL NOT NULL,
      age INTEGER NOT NULL,
      gender TEXT NOT NULL,
      daily_target REAL NOT NULL,
      initial_weight REAL NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )
  `);

  // 体重记录表
  db.exec(`
    CREATE TABLE IF NOT EXISTS weight_records (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      weight REAL NOT NULL,
      record_date TEXT NOT NULL UNIQUE,
      created_at TEXT NOT NULL
    )
  `);

  // 运动库表
  db.exec(`
    CREATE TABLE IF NOT EXISTS exercises (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE,
      met_value REAL NOT NULL,
      intensity TEXT NOT NULL,
      created_at TEXT NOT NULL
    )
  `);

  // 活动记录表
  db.exec(`
    CREATE TABLE IF NOT EXISTS activities (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      type TEXT NOT NULL,
      name TEXT NOT NULL,
      duration INTEGER NOT NULL,
      calories REAL,
      met_value REAL,
      weight REAL,
      timestamp TEXT NOT NULL,
      date TEXT NOT NULL,
      completed INTEGER DEFAULT 1
    )
  `);

  // 每日统计表
  db.exec(`
    CREATE TABLE IF NOT EXISTS daily_stats (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date TEXT NOT NULL UNIQUE,
      total_calories REAL DEFAULT 0,
      target_calories REAL NOT NULL,
      achieved INTEGER DEFAULT 0,
      achieved_today INTEGER DEFAULT 0,
      exercise_count INTEGER DEFAULT 0,
      gaze_count INTEGER DEFAULT 0,
      stand_count INTEGER DEFAULT 0,
      weight REAL,
      streak INTEGER DEFAULT 0
    )
  `);

  // 提醒设置表
  db.exec(`
    CREATE TABLE IF NOT EXISTS reminder_settings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      type TEXT NOT NULL UNIQUE,
      interval_min INTEGER NOT NULL,
      interval_max INTEGER NOT NULL,
      duration INTEGER NOT NULL,
      enabled INTEGER DEFAULT 1,
      updated_at TEXT NOT NULL
    )
  `);

  // 系统设置表
  db.exec(`
    CREATE TABLE IF NOT EXISTS system_settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )
  `);

  console.log('数据库表创建成功');
}

function initData(db: Database.Database) {
  // 初始化 15 个运动数据
  const exercises = [
    { name: '半程波比跳', metValue: 10.0, intensity: 'high' },
    { name: '开合跳', metValue: 8.0, intensity: 'high' },
    { name: '高抬腿', metValue: 8.0, intensity: 'high' },
    { name: '俯卧撑', metValue: 8.0, intensity: 'high' },
    { name: '哑铃硬拉', metValue: 6.0, intensity: 'medium' },
    { name: '箭步蹲', metValue: 6.0, intensity: 'medium' },
    { name: '深蹲', metValue: 5.0, intensity: 'medium' },
    { name: '徒手硬拉', metValue: 5.0, intensity: 'medium' },
    { name: '弹力带划船', metValue: 4.5, intensity: 'medium' },
    { name: '哑铃侧平举', metValue: 4.0, intensity: 'medium' },
    { name: '哑铃前平举', metValue: 4.0, intensity: 'medium' },
    { name: '仰卧起坐', metValue: 3.8, intensity: 'low' },
    { name: '站姿扭腰', metValue: 3.5, intensity: 'low' },
    { name: '弹力带开合', metValue: 3.5, intensity: 'low' },
    { name: '全身拉伸', metValue: 2.3, intensity: 'low' },
  ];

  const insertExercise = db.prepare(`
    INSERT INTO exercises (name, met_value, intensity, created_at)
    VALUES (?, ?, ?, datetime('now'))
  `);

  const count = db.exec('SELECT COUNT(*) as count FROM exercises').get(0) as { count: number };
  if (count.count === 0) {
    exercises.forEach(exercise => {
      insertExercise.run(exercise.name, exercise.metValue, exercise.intensity);
    });
    console.log('初始化 15 个运动数据成功');
  }

  // 初始化默认提醒设置
  const reminderSettings = [
    { type: 'exercise', intervalMin: 10, intervalMax: 20, duration: 120 },
    { type: 'gaze', intervalMin: 10, intervalMax: 20, duration: 60 },
    { type: 'stand', intervalMin: 10, intervalMax: 20, duration: 300 },
  ];

  const insertSetting = db.prepare(`
    INSERT INTO reminder_settings (type, interval_min, interval_max, duration, updated_at)
    VALUES (?, ?, ?, ?, datetime('now'))
  `);

  const settingCount = db.exec('SELECT COUNT(*) as count FROM reminder_settings').get(0) as { count: number };
  if (settingCount.count === 0) {
    reminderSettings.forEach(setting => {
      insertSetting.run(setting.type, setting.intervalMin, setting.intervalMax, setting.duration);
    });
    console.log('初始化提醒设置成功');
  }
}

export function closeDatabase() {
  if (dbInstance) {
    dbInstance.close();
    dbInstance = null;
  }
}
