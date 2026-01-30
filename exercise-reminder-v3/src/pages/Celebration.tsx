import { useEffect, useState } from 'react';
import { COLORS } from '../constants';

export default function Celebration() {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // 从 URL 参数获取数据
    const params = new URLSearchParams(window.location.hash.split('?')[1]);
    const achieved = Number(params.get('achieved')) || 0;
    const target = Number(params.get('target')) || 300;

    // 3秒后自动关闭
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(() => window.close(), 300);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  if (!isVisible) return null;

  const params = new URLSearchParams(window.location.hash.split('?')[1]);
  const achieved = Number(params.get('achieved')) || 0;
  const target = Number(params.get('target')) || 300;

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-purple-500 to-pink-500 text-white">
      <div className="text-center">
        {/* Confetti Animation */}
        <div className="text-6xl mb-6">🎉</div>

        {/* Congratulations */}
        <h1 className="text-4xl font-bold mb-4">太棒了！</h1>
        <p className="text-xl mb-6">今日目标已达成</p>

        {/* Stats */}
        <div className="bg-white bg-opacity-20 backdrop-blur-lg rounded-2xl p-6 mb-6">
          <div className="text-5xl font-bold mb-2">{achieved}</div>
          <div className="text-lg opacity-90">/ {target} 千卡</div>
        </div>

        {/* Progress */}
        <div className="w-64 mx-auto bg-white bg-opacity-30 rounded-full h-3">
          <div
            className="h-3 rounded-full bg-white"
            style={{ width: '100%' }}
          />
        </div>
      </div>
    </div>
  );
}
