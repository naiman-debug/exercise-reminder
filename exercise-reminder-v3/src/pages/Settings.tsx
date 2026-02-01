import { useEffect, useState } from 'react';
import { useUserStore } from '../store/useUserStore';
import { useSettingsStore } from '../store/useSettingsStore';
import { useExerciseStore } from '../store/useExerciseStore';
import { GENDER, DEFAULTS, COLORS, INTENSITY_LEVELS } from '../constants';
import { Exercise, ReminderSettings } from '../types';

export default function Settings() {
  const { userInfo, saveUserInfo, fetchUserInfo } = useUserStore();
  const {
    reminderSettings,
    fetchReminderSettings,
    updateReminderSettingsBatch,
    fetchAutoStartSetting,
    setAutoStartEnabled,
    autoStartEnabled,
    globalMinIntervalSec,
    fetchGlobalMinInterval,
    setGlobalMinInterval,
  } = useSettingsStore();
  const { exercises, fetchAllExercises, addExercise, deleteExercise } = useExerciseStore();
  const [activeTab, setActiveTab] = useState<'profile' | 'reminder' | 'exercise'>('profile');
  const [draftSettings, setDraftSettings] = useState<ReminderSettings[]>([]);
  const [statusMessage, setStatusMessage] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const [draftGlobalMinInterval, setDraftGlobalMinInterval] = useState<number>(globalMinIntervalSec);

  const [formData, setFormData] = useState<{
    height: number;
    weight: number;
    age: number;
    gender: 'male' | 'female';
    dailyTarget: number;
    initialWeight: number;
  }>({
    height: DEFAULTS.HEIGHT as number,
    weight: DEFAULTS.WEIGHT as number,
    age: DEFAULTS.AGE as number,
    gender: GENDER.MALE,
    dailyTarget: DEFAULTS.DAILY_TARGET as number,
    initialWeight: DEFAULTS.WEIGHT as number,
  });

  const [newExercise, setNewExercise] = useState({ name: '', metValue: 5, intensity: INTENSITY_LEVELS.MEDIUM });

  useEffect(() => {
    const loadData = async () => {
      await fetchUserInfo();
      await fetchReminderSettings();
      await fetchAllExercises();
      await fetchAutoStartSetting();
      await fetchGlobalMinInterval();
    };
    loadData();
  }, [fetchUserInfo, fetchReminderSettings, fetchAllExercises, fetchAutoStartSetting, fetchGlobalMinInterval]);

  useEffect(() => {
    if (userInfo) {
      setFormData({
        height: userInfo.height,
        weight: userInfo.weight,
        age: userInfo.age,
        gender: userInfo.gender,
        dailyTarget: userInfo.dailyTarget,
        initialWeight: userInfo.initialWeight,
      });
    }
  }, [userInfo]);

  useEffect(() => {
    setDraftSettings(reminderSettings);
  }, [reminderSettings]);

  useEffect(() => {
    setDraftGlobalMinInterval(globalMinIntervalSec);
  }, [globalMinIntervalSec]);

  const handleSaveProfile = async () => {
    await saveUserInfo(formData);
    setStatusMessage({ message: '个人信息已保存', type: 'success' });
  };

  const handleSaveAllReminderSettings = async () => {
    let didSwap = false;
    const normalizedSettings = draftSettings.map((item) => {
      if (item.intervalMin > item.intervalMax) {
        didSwap = true;
        return {
          ...item,
          intervalMin: item.intervalMax,
          intervalMax: item.intervalMin,
        };
      }
      return item;
    });

    setDraftSettings(normalizedSettings);
    await updateReminderSettingsBatch(normalizedSettings);
    await setGlobalMinInterval(draftGlobalMinInterval);
    setStatusMessage({
      message: didSwap ? '提醒设置已保存（已自动纠正区间）' : '提醒设置已保存',
      type: 'success',
    });
  };

  const handleAddExercise = async () => {
    if (!newExercise.name) {
      setStatusMessage({ message: '请输入运动名称', type: 'error' });
      return;
    }
    await addExercise(newExercise as any);
    setNewExercise({ name: '', metValue: 5, intensity: INTENSITY_LEVELS.MEDIUM });
    setStatusMessage({ message: '运动已添加', type: 'success' });
  };

  const handleDeleteExercise = async (id: number) => {
    if (confirm('确定要删除这个运动吗？')) {
      await deleteExercise(id);
      setStatusMessage({ message: '运动已删除', type: 'success' });
    }
  };

  const getIntensityColor = (intensity: string) => {
    switch (intensity) {
      case INTENSITY_LEVELS.HIGH:
        return COLORS.HIGH_INTENSITY;
      case INTENSITY_LEVELS.MEDIUM:
        return COLORS.MEDIUM_INTENSITY;
      case INTENSITY_LEVELS.LOW:
        return COLORS.LOW_INTENSITY;
      default:
        return COLORS.INFO;
    }
  };

  const getIntensityLabel = (intensity: string) => {
    switch (intensity) {
      case INTENSITY_LEVELS.HIGH:
        return '高强度';
      case INTENSITY_LEVELS.MEDIUM:
        return '中强度';
      case INTENSITY_LEVELS.LOW:
        return '低强度';
      default:
        return '未知';
    }
  };

  const getReminderHint = (settingType: 'exercise' | 'gaze' | 'stand') => {
    const current = draftSettings.find((item) => item.type === settingType);
    if (!current) return '在 X-Y 分钟内随机触发';
    return `在 ${current.intervalMin}-${current.intervalMax} 分钟内随机触发`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1a1a2e] to-[#16213e] text-white">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {statusMessage && (
          <div
            data-testid="status-toast"
            className={`mb-4 rounded-lg px-4 py-2 text-sm font-medium border ${
              statusMessage.type === 'success'
                ? 'bg-green-500 bg-opacity-20 border-green-300 text-green-100'
                : 'bg-red-500 bg-opacity-20 border-red-300 text-red-100'
            }`}
          >
            {statusMessage.message}
          </div>
        )}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold">设置</h1>
          <button
            onClick={() => window.location.hash = '#/'}
            className="px-4 py-2 rounded-lg text-sm font-medium"
            style={{ backgroundColor: `${COLORS.PRIMARY}40` }}
          >
            ← 返回
          </button>
        </div>

        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('profile')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === 'profile' ? 'bg-opacity-100' : 'bg-opacity-20'
            }`}
            style={{ backgroundColor: activeTab === 'profile' ? COLORS.PRIMARY : `${COLORS.PRIMARY}40` }}
          >
            👤 个人信息
          </button>
          <button
            onClick={() => setActiveTab('reminder')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === 'reminder' ? 'bg-opacity-100' : 'bg-opacity-20'
            }`}
            style={{ backgroundColor: activeTab === 'reminder' ? COLORS.PRIMARY : `${COLORS.PRIMARY}40` }}
            data-testid="tab-reminder"
          >
            ⏰ 提醒设置
          </button>
          <button
            onClick={() => setActiveTab('exercise')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeTab === 'exercise' ? 'bg-opacity-100' : 'bg-opacity-20'
            }`}
            style={{ backgroundColor: activeTab === 'exercise' ? COLORS.PRIMARY : `${COLORS.PRIMARY}40` }}
            data-testid="tab-exercise"
          >
            🏋️ 运动库
          </button>
        </div>

        <div className="bg-white bg-opacity-10 backdrop-blur-lg rounded-2xl p-6 border border-white border-opacity-20">
          {activeTab === 'profile' && (
            <div>
              <h2 className="text-xl font-bold mb-6">个人信息</h2>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <label className="w-20 text-sm">身高</label>
                  <input
                    type="number"
                    value={formData.height}
                    onChange={(e) => setFormData({ ...formData, height: Number(e.target.value) })}
                    className="w-32 px-3 py-2 rounded-lg bg-white bg-opacity-10 border border-white border-opacity-20 text-white"
                  />
                  <span className="text-sm opacity-60">cm</span>
                </div>

                <div className="flex items-center gap-4">
                  <label className="w-20 text-sm">体重</label>
                  <input
                    type="number"
                    value={formData.weight}
                    onChange={(e) => setFormData({ ...formData, weight: Number(e.target.value) })}
                    className="w-32 px-3 py-2 rounded-lg bg-white bg-opacity-10 border border-white border-opacity-20 text-white"
                  />
                  <span className="text-sm opacity-60">kg</span>
                </div>

                <div className="flex items-center gap-4">
                  <label className="w-20 text-sm">年龄</label>
                  <input
                    type="number"
                    value={formData.age}
                    onChange={(e) => setFormData({ ...formData, age: Number(e.target.value) })}
                    className="w-24 px-3 py-2 rounded-lg bg-white bg-opacity-10 border border-white border-opacity-20 text-white"
                  />
                  <span className="text-sm opacity-60">岁</span>
                </div>

                <div className="flex items-center gap-4">
                  <label className="w-20 text-sm">性别</label>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setFormData({ ...formData, gender: GENDER.MALE })}
                      className={`px-4 py-2 rounded-lg text-sm ${
                        formData.gender === GENDER.MALE ? 'bg-opacity-100' : 'bg-opacity-20'
                      }`}
                      style={{ backgroundColor: formData.gender === GENDER.MALE ? COLORS.PRIMARY : `${COLORS.PRIMARY}40` }}
                    >
                      男
                    </button>
                    <button
                      onClick={() => setFormData({ ...formData, gender: GENDER.FEMALE })}
                      className={`px-4 py-2 rounded-lg text-sm ${
                        formData.gender === GENDER.FEMALE ? 'bg-opacity-100' : 'bg-opacity-20'
                      }`}
                      style={{ backgroundColor: formData.gender === GENDER.FEMALE ? COLORS.PRIMARY : `${COLORS.PRIMARY}40` }}
                    >
                      女
                    </button>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <label className="w-20 text-sm">每日目标</label>
                  <input
                    type="number"
                    value={formData.dailyTarget}
                    onChange={(e) => setFormData({ ...formData, dailyTarget: Number(e.target.value) })}
                    className="w-32 px-3 py-2 rounded-lg bg-white bg-opacity-10 border border-white border-opacity-20 text-white"
                  />
                  <span className="text-sm opacity-60">大卡</span>
                </div>

              </div>
            </div>
          )}

          {activeTab === 'reminder' && (
            <div>
              <h2 className="text-xl font-bold mb-6">提醒设置</h2>
              <div className="space-y-6">
                <div className="bg-white bg-opacity-5 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xl">⏱️</span>
                    <h3 className="font-bold">全局最小提醒间隔</h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min={0}
                      value={draftGlobalMinInterval}
                      onChange={(e) => setDraftGlobalMinInterval(Number(e.target.value))}
                      data-testid="global-min-interval"
                      className="w-28 px-3 py-2 rounded bg-white bg-opacity-10 border border-white border-opacity-20 text-white text-center"
                    />
                    <span className="text-sm opacity-60">秒</span>
                  </div>
                  <div className="text-xs opacity-60 mt-2">
                    任意两次提醒之间至少间隔以上秒数（用于避免提醒连发）
                  </div>
                </div>
                {draftSettings.map((setting) => (
                  <div key={setting.type} className="bg-white bg-opacity-5 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-4">
                      <span className="text-2xl">
                        {setting.type === 'exercise' ? '⚡' : setting.type === 'gaze' ? '👀' : '🧍'}
                      </span>
                      <h3 className="font-bold">
                        {setting.type === 'exercise' ? '运动提醒' : setting.type === 'gaze' ? '远眺提醒' : '站立提醒'}
                      </h3>
                    </div>

                    <div className="space-y-3">
                      <div className="flex items-center gap-2">
                        <label className="w-24 text-sm">提醒间隔</label>
                        <input
                          type="number"
                          value={setting.intervalMin}
                          onChange={(e) => {
                            const newSettings = [...draftSettings];
                            const idx = newSettings.findIndex((s) => s.type === setting.type);
                            newSettings[idx].intervalMin = Number(e.target.value);
                            setDraftSettings(newSettings);
                          }}
                          data-testid={`interval-min-${setting.type}`}
                          className="w-20 px-3 py-2 rounded bg-white bg-opacity-10 border border-white border-opacity-20 text-white text-center"
                        />
                        <span className="text-sm">–</span>
                        <input
                          type="number"
                          value={setting.intervalMax}
                          onChange={(e) => {
                            const newSettings = [...draftSettings];
                            const idx = newSettings.findIndex((s) => s.type === setting.type);
                            newSettings[idx].intervalMax = Number(e.target.value);
                            setDraftSettings(newSettings);
                          }}
                          data-testid={`interval-max-${setting.type}`}
                          className="w-20 px-3 py-2 rounded bg-white bg-opacity-10 border border-white border-opacity-20 text-white text-center"
                        />
                        <span className="text-sm opacity-60">分钟</span>
                      </div>
                      <div className="text-xs opacity-60">{getReminderHint(setting.type)}</div>

                      <div className="flex items-center gap-2">
                        <label className="w-24 text-sm">单次时长</label>
                        <input
                          type="number"
                          value={setting.duration}
                          onChange={(e) => {
                            const newSettings = [...draftSettings];
                            const idx = newSettings.findIndex((s) => s.type === setting.type);
                            newSettings[idx].duration = Number(e.target.value);
                            setDraftSettings(newSettings);
                          }}
                          className="w-20 px-3 py-2 rounded bg-white bg-opacity-10 border border-white border-opacity-20 text-white text-center"
                        />
                        <span className="text-sm opacity-60">秒</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'exercise' && (
            <div>
              <h2 className="text-xl font-bold mb-6">运动库</h2>

              <div className="bg-white bg-opacity-5 rounded-lg p-4 mb-6">
                <h3 className="font-bold mb-4">添加运动</h3>
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="运动名称"
                    value={newExercise.name}
                    onChange={(e) => setNewExercise({ ...newExercise, name: e.target.value })}
                    className="flex-1 px-3 py-2 rounded bg-white bg-opacity-10 border border-white border-opacity-20 text-white"
                  />
                  <input
                    type="number"
                    placeholder="MET值"
                    value={newExercise.metValue}
                    onChange={(e) => setNewExercise({ ...newExercise, metValue: Number(e.target.value) })}
                    className="w-24 px-3 py-2 rounded bg-white bg-opacity-10 border border-white border-opacity-20 text-white"
                  />
                  <button
                    onClick={handleAddExercise}
                    className="px-4 py-2 rounded font-medium"
                    style={{ backgroundColor: COLORS.PRIMARY }}
                  >
                    添加
                  </button>
                </div>
              </div>

              <div className="space-y-2">
                {exercises.map((exercise) => (
                  <div
                    key={exercise.id}
                    className="flex items-center justify-between bg-white bg-opacity-5 rounded-lg px-4 py-3"
                  >
                    <div className="flex items-center gap-3">
                      <span className="font-medium">{exercise.name}</span>
                      <span
                        className="px-2 py-1 rounded text-xs font-medium"
                        style={{ backgroundColor: `${getIntensityColor(exercise.intensity)}40`, color: getIntensityColor(exercise.intensity) }}
                      >
                        {exercise.metValue} MET
                      </span>
                      <span
                        className="px-2 py-1 rounded text-xs"
                        style={{ backgroundColor: `${getIntensityColor(exercise.intensity)}20`, color: getIntensityColor(exercise.intensity) }}
                      >
                        {getIntensityLabel(exercise.intensity)}
                      </span>
                    </div>
                    <button
                      onClick={() => handleDeleteExercise(exercise.id)}
                      className="text-xs opacity-60 hover:opacity-100 hover:text-red-400 transition-colors"
                    >
                      删除
                    </button>
                  </div>
                ))}
              </div>

              <div className="mt-6 flex items-center justify-between bg-white bg-opacity-5 rounded-lg px-4 py-3 border border-white border-opacity-10">
                <span className="font-medium">开机自启动</span>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={autoStartEnabled}
                    onChange={(e) => setAutoStartEnabled(e.target.checked)}
                    data-testid="auto-start-toggle"
                  />
                  <div className="w-11 h-6 bg-white bg-opacity-20 peer-focus:outline-none rounded-full peer peer-checked:bg-opacity-100 peer-checked:bg-gradient-to-r peer-checked:from-purple-500 peer-checked:to-purple-400 after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:after:translate-x-full" />
                </label>
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 flex gap-3 justify-end">
          <button
            onClick={() => window.location.hash = '#/'}
            className="px-4 py-2 rounded-lg text-sm font-medium border border-white border-opacity-30"
          >
            取消
          </button>
          <button
            onClick={async () => {
              if (activeTab === 'profile') {
                await handleSaveProfile();
              } else if (activeTab === 'reminder') {
                await handleSaveAllReminderSettings();
              } else {
                setStatusMessage({ message: '设置已保存', type: 'success' });
              }
            }}
            className="px-4 py-2 rounded-lg text-sm font-medium"
            style={{ backgroundColor: COLORS.PRIMARY }}
            data-testid="footer-save"
          >
            保存设置
          </button>
        </div>
      </div>
    </div>
  );
}
