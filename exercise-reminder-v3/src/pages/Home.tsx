import { useEffect, useState } from 'react';
import { useUserStore } from '../store/useUserStore';
import { useStatsStore } from '../store/useStatsStore';
import { useActivityStore } from '../store/useActivityStore';
import { useSettingsStore } from '../store/useSettingsStore';
import { COLORS } from '../constants';

export default function Home() {
  const { userInfo, fetchUserInfo, updateWeight } = useUserStore();
  const { todayStats, historyStats, fetchTodayStats, fetchHistoryStats } = useStatsStore();
  const { todayActivities, fetchActivitiesByDate } = useActivityStore();
  const { reminderStatus, pauseReminders, resumeReminders } = useSettingsStore();
  const [currentDate, setCurrentDate] = useState(new Date());
  const [isEditingWeight, setIsEditingWeight] = useState(false);
  const [weightDraft, setWeightDraft] = useState('');

  useEffect(() => {
    const loadData = async () => {
      await fetchUserInfo();
      const today = new Date().toISOString().split('T')[0];
      await fetchTodayStats(today);
      await fetchHistoryStats();
      await fetchActivitiesByDate(today);
    };

    loadData();

    const interval = setInterval(() => {
      setCurrentDate(new Date());
      loadData();
    }, 60000);

    return () => clearInterval(interval);
  }, [fetchUserInfo, fetchTodayStats, fetchHistoryStats, fetchActivitiesByDate]);

  const handleUpdateWeight = async () => {
    const parsed = Number(weightDraft);
    if (!weightDraft || Number.isNaN(parsed)) {
      return;
    }
    await updateWeight(parsed);
    await fetchTodayStats(new Date().toISOString().split('T')[0]);
    setIsEditingWeight(false);
  };

  const handleTogglePause = async () => {
    if (reminderStatus.isPaused) {
      await resumeReminders();
    } else {
      await pauseReminders();
    }
    await useSettingsStore.getState().fetchReminderStatus();
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  };

  const progressPercent = todayStats
    ? Math.min((todayStats.totalCalories / todayStats.targetCalories) * 100, 100)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1a1a2e] to-[#16213e] text-white">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold">健康提醒助手</h1>
          <div className="flex gap-2">
            <button
              onClick={handleTogglePause}
              className="px-4 py-2 rounded-lg bg-opacity-20 text-sm font-medium transition-colors"
              style={{
                backgroundColor: reminderStatus.isPaused ? COLORS.SUCCESS : COLORS.WARNING,
              }}
            >
              {reminderStatus.isPaused ? '▶️ 恢复提醒' : '⏸ 暂停提醒'}
            </button>
            <button
              onClick={() => window.location.hash = '#/settings'}
              className="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              style={{ backgroundColor: `${COLORS.PRIMARY}40` }}
            >
              ⚙️ 设置
            </button>
          </div>
        </div>

        <div className="bg-white bg-opacity-10 backdrop-blur-lg rounded-2xl p-6 mb-6 border border-white border-opacity-20">
          <h2 className="text-xl font-bold mb-4">🎯 今日目标进度</h2>

          <div className="mb-4">
            <div className="flex justify-between mb-2">
              <span className="text-sm">运动热量</span>
              <span className="text-sm font-bold">
                {todayStats?.totalCalories || 0} / {todayStats?.targetCalories || 300} 千卡
              </span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3">
              <div
                className="h-3 rounded-full transition-all duration-500"
                style={{
                  width: `${progressPercent}%`,
                  background: `linear-gradient(to right, ${COLORS.PRIMARY}, ${COLORS.PRIMARY_LIGHT})`,
                }}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white bg-opacity-5 rounded-lg p-4">
              <div className="text-sm opacity-80 mb-1">🔥 连续打卡</div>
              <div className="text-2xl font-bold">{todayStats?.streak || 0} 天</div>
            </div>
            <div className="bg-white bg-opacity-5 rounded-lg p-4">
              <div className="text-sm opacity-80 mb-1">⚖️ 当前体重</div>
              {!isEditingWeight ? (
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold">{userInfo?.weight || 0} kg</span>
                  <button
                    onClick={() => {
                      setWeightDraft(String(userInfo?.weight || ''));
                      setIsEditingWeight(true);
                    }}
                    className="px-3 py-1 rounded text-xs font-medium"
                    style={{ backgroundColor: `${COLORS.PRIMARY}40` }}
                  >
                    更新
                  </button>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    value={weightDraft}
                    onChange={(e) => setWeightDraft(e.target.value)}
                    data-testid="weight-input"
                    className="w-24 px-2 py-1 rounded bg-white bg-opacity-10 border border-white border-opacity-20 text-white text-sm"
                  />
                  <button
                    onClick={handleUpdateWeight}
                    className="px-3 py-1 rounded text-xs font-medium"
                    style={{ backgroundColor: `${COLORS.PRIMARY}` }}
                  >
                    保存
                  </button>
                  <button
                    onClick={() => setIsEditingWeight(false)}
                    className="px-3 py-1 rounded text-xs font-medium border border-white border-opacity-30"
                  >
                    取消
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="bg-white bg-opacity-10 backdrop-blur-lg rounded-2xl p-6 mb-6 border border-white border-opacity-20">
          <h2 className="text-xl font-bold mb-4">🧾 今日活动详情</h2>
          <div className="space-y-2">
            {todayActivities.length === 0 ? (
              <div className="text-center text-sm opacity-60 py-8">暂无活动记录</div>
            ) : (
              todayActivities.map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-center justify-between bg-white bg-opacity-5 rounded-lg p-4"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">
                      {activity.type === 'exercise' ? '🏃' : activity.type === 'gaze' ? '👀' : '🧍'}
                    </span>
                    <div>
                      <div className="font-medium">{activity.name}</div>
                      <div className="text-xs opacity-60">
                        {formatTime(activity.timestamp)} · {activity.duration} 秒
                      </div>
                    </div>
                  </div>
                  {activity.calories && (
                    <div className="text-sm font-bold" style={{ color: COLORS.PRIMARY_LIGHT }}>
                      {activity.calories.toFixed(1)} 大卡
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        <div className="bg-white bg-opacity-10 backdrop-blur-lg rounded-2xl p-6 border border-white border-opacity-20">
          <h2 className="text-xl font-bold mb-4">📈 历史数据</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: COLORS.PRIMARY_LIGHT }}>
                {historyStats?.totalCalories || 0}
              </div>
              <div className="text-xs opacity-60 mt-1">累计消耗（大卡）</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: COLORS.SUCCESS }}>
                {historyStats?.totalStreak || 0}
              </div>
              <div className="text-xs opacity-60 mt-1">累计打卡（天）</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: COLORS.INFO }}>
                {historyStats ? historyStats.weightChange.delta.toFixed(1) : 0}
              </div>
              <div className="text-xs opacity-60 mt-1">体重变化（kg）</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
