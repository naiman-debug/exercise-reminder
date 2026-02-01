import { useEffect, useState } from 'react';
import { TriggerEventData } from '../types';
import '../styles/reminder-modal.css';

export default function ReminderModal() {
  const [eventData, setEventData] = useState<TriggerEventData | null>(null);
  const [countdown, setCountdown] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [userWeight, setUserWeight] = useState<number>(70);

  useEffect(() => {
    const params = new URLSearchParams(window.location.hash.split('?')[1]);
    const type = params.get('type') as 'exercise' | 'gaze' | 'stand' | null;
    const duration = Number(params.get('duration')) || 0;
    const exerciseName = params.get('exerciseName') || undefined;
    const metValue = params.get('metValue') ? Number(params.get('metValue')) : undefined;

    if (type) {
      setEventData({
        type,
        duration,
        timestamp: Date.now(),
        exerciseName,
        metValue,
      });
      setCountdown(duration);
    }
  }, []);

  useEffect(() => {
    const loadUserWeight = async () => {
      try {
        const info = await window.electronAPI.getUserInfo();
        if (info?.weight) {
          setUserWeight(Number(info.weight));
        }
      } catch (error) {
        console.error('Failed to load user info:', error);
      }
    };
    loadUserWeight();
  }, []);

  useEffect(() => {
    if (countdown <= 0 || isCompleted) return;

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
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

    const now = new Date();
    const timestamp = now.toISOString();
    const date = timestamp.split('T')[0];

    const calories = eventData.metValue
      ? Number(((eventData.metValue * userWeight * (eventData.duration / 60)) / 60).toFixed(1))
      : null;

    const activity = {
      type: eventData.type,
      name: eventData.exerciseName || (eventData.type === 'exercise' ? '运动' : eventData.type === 'gaze' ? '远眺' : '站立'),
      duration: eventData.duration,
      ...(eventData.metValue && { metValue: eventData.metValue }),
      ...(calories !== null && { calories }),
      weight: userWeight,
      timestamp,
      date,
      completed: true,
    };

    try {
      await window.electronAPI.saveActivity(activity);
    } catch (error) {
      console.error('Failed to save activity:', error);
    }

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
    if (eventData.type === 'exercise') return '微运动时间';
    if (eventData.type === 'gaze') return '远眺放松';
    if (eventData.type === 'stand') return '站立提醒';
    return '健康提醒';
  };

  const getPromptText = () => {
    if (!eventData) return '';
    if (eventData.type === 'exercise') return eventData.exerciseName || '运动时间';
    if (eventData.type === 'gaze') return '远眺放松';
    if (eventData.type === 'stand') return '站立活动';
    return '';
  };

  const getSubtitle = () => {
    if (!eventData) return '';
    if (eventData.type === 'gaze') return '望向 5 米外，放松眼睛';
    if (eventData.type === 'stand') return '放松肩颈与腰背';
    return '';
  };

  const calculateCalories = () => {
    if (!eventData || !eventData.metValue) return null;
    const durationInMinutes = eventData.duration / 60;
    return (eventData.metValue * userWeight * durationInMinutes / 60).toFixed(1);
  };

  const isWarning = countdown <= 10 && countdown > 5;
  const isCritical = countdown <= 5 && countdown > 0;

  if (!eventData) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-white">
        <div className="text-gray-500">加载中...</div>
      </div>
    );
  }

  return (
    <div className="reminder-page">
      <div
        data-testid="reminder-modal"
        data-variant={eventData.type}
        className={`modal-shell ${eventData.type === 'stand' ? 'modal-small' : 'modal-large'} ${
          eventData.type === 'gaze' ? 'modal-eye' : eventData.type === 'stand' ? 'modal-stand' : 'modal-exercise'
        }`}
      >
        <div className="modal-header" style={{ WebkitAppRegion: 'drag' } as React.CSSProperties}>
          <div className="modal-title">
            <span className="icon">{eventData.type === 'exercise' ? '⚡' : eventData.type === 'gaze' ? '👀' : '🧍'}</span>
            <span>{getTitle()}</span>
          </div>
          <div className="window-controls" style={{ WebkitAppRegion: 'no-drag' } as React.CSSProperties}>
            <button className="window-btn" aria-disabled>
              _
            </button>
            <button className="window-btn" aria-disabled>
              ▢
            </button>
            <button onClick={handleSkip} className="window-btn close" title="跳过">
              ×
            </button>
          </div>
        </div>

        <div className="modal-body">
          <div style={{ textAlign: 'center' }}>
            <div className="activity-name">{getPromptText()}</div>
            {getSubtitle() && <div className="activity-subtitle">{getSubtitle()}</div>}
            {eventData.metValue && (
              <div className="activity-info" style={{ marginTop: '8px' }}>
                <span className="met-badge">MET: {eventData.metValue}</span>
              </div>
            )}
          </div>

          <div className="countdown-container">
            <div
              data-testid="countdown-display"
              className={`countdown-display ${isCritical ? 'critical' : isWarning ? 'warning' : ''}`}
              style={eventData.type === 'stand' ? { fontSize: '80px' } : undefined}
            >
              {isCompleted ? '✓' : formatTime(countdown)}
            </div>
            <div className="countdown-label">倒计时</div>
          </div>

          {eventData.type === 'exercise' && calculateCalories() && (
            <div className="calories-display">
              <span>预计消耗：</span>
              <span className="value">{calculateCalories()}</span>
              <span>千卡</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
