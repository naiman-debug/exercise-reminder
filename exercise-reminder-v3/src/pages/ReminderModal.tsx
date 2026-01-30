import { useEffect, useState } from 'react';
import { TriggerEventData } from '../types';
import { COLORS } from '../constants';

export default function ReminderModal() {
  const [eventData, setEventData] = useState<TriggerEventData | null>(null);
  const [countdown, setCountdown] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    // 从 URL 参数获取事件数据
    const params = new URLSearchParams(window.location.hash.split('?')[1]);
    const type = params.get('type') as 'exercise' | 'gaze' | 'stand' | null;
    const duration = Number(params.get('duration')) || 0;
    const exerciseName = params.get('exerciseName') || undefined;
    const metValue = params.get('metValue') ? Number(params.get('metValue')) : undefined;

    if (type) {
      const data: TriggerEventData = {
        type,
        duration,
        timestamp: Date.now(),
        exerciseName,
        metValue,
      };
      setEventData(data);
      setCountdown(duration);
    }
  }, []);

  useEffect(() => {
    if (countdown <= 0 || isCompleted) return;

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          // 倒计时结束，自动完成
          handleComplete();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [countdown, isCompleted]);

  const handleComplete = async () => {
    if (!eventData || isCompleted) return;

    setIsCompleted(true);

    // 保存活动记录
    const activity = {
      type: eventData.type,
      name: eventData.exerciseName || (eventData.type === 'exercise' ? '运动' : eventData.type === 'gaze' ? '远眺' : '站立'),
      duration: eventData.duration,
      ...(eventData.metValue && { metValue: eventData.metValue }),
    };

    try {
      await window.electronAPI.saveActivity(activity);
    } catch (error) {
      console.error('Failed to save activity:', error);
    }

    // 延迟关闭窗口
    setTimeout(() => {
      window.close();
    }, 500);
  };

  const handleSkip = () => {
    window.close();
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getTitle = () => {
    if (!eventData) return '';

    switch (eventData.type) {
      case 'exercise':
        return '🏃 微运动时间';
      case 'gaze':
        return '👀 远眺放松';
      case 'stand':
        return '🧍 站立提醒';
      default:
        return '健康提醒';
    }
  };

  const getPromptText = () => {
    if (!eventData) return '';

    switch (eventData.type) {
      case 'exercise':
        return eventData.exerciseName || '运动时间';
      case 'gaze':
        return '望向5米外，放松眼睛';
      case 'stand':
        return '请站起来活动一下';
      default:
        return '';
    }
  };

  const calculateCalories = () => {
    if (!eventData || !eventData.metValue) return null;

    // 从用户信息获取体重（这里简化处理，实际应从 store 获取）
    const weight = 70; // 默认体重
    const durationInMinutes = eventData.duration / 60;
    return (eventData.metValue * weight * durationInMinutes / 60).toFixed(1);
  };

  const isWarning = countdown <= 10 && countdown > 0;

  if (!eventData) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-white">
        <div className="text-gray-500">加载中...</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white text-gray-800">
      {/* Title Bar */}
      <div className="absolute top-0 left-0 right-0 flex justify-between items-center px-4 py-2 bg-gray-100">
        <div className="font-medium">{getTitle()}</div>
        <button
          onClick={handleSkip}
          className="text-gray-600 hover:text-gray-800 text-xl px-2"
          title="跳过"
        >
          ×
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 flex flex-col items-center justify-center w-full max-w-lg px-8">
        {/* Prompt */}
        <div className="text-center mb-8">
          <div className="text-2xl font-bold mb-2">{getPromptText()}</div>
          {eventData.metValue && (
            <div className="text-lg text-gray-600">MET: {eventData.metValue}</div>
          )}
        </div>

        {/* Countdown */}
        <div
          className={`text-8xl font-bold mb-8 transition-colors ${
            isWarning ? 'text-orange-500' : 'text-green-500'
          }`}
        >
          {isCompleted ? '✓' : formatTime(countdown)}
        </div>

        {/* Calories (for exercise) */}
        {eventData.type === 'exercise' && calculateCalories() && (
          <div className="text-center text-gray-600">
            <div className="text-sm">预计消耗</div>
            <div className="text-2xl font-bold" style={{ color: COLORS.PRIMARY }}>
              {calculateCalories()} 千卡
            </div>
          </div>
        )}

        {/* Completed Message */}
        {isCompleted && (
          <div className="text-center text-green-500 font-medium">
            已完成！
          </div>
        )}
      </div>

      {/* Footer */}
      {!isCompleted && (
        <div className="absolute bottom-8">
          <button
            onClick={handleSkip}
            className="px-6 py-2 rounded-lg text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-colors"
          >
            跳过
          </button>
        </div>
      )}
    </div>
  );
}
