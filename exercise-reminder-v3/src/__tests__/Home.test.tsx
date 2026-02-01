import { act } from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Home from '../pages/Home';

const mockFetchUserInfo = jest.fn();
const mockUpdateWeight = jest.fn();
const mockFetchTodayStats = jest.fn();
const mockFetchHistoryStats = jest.fn();
const mockFetchActivitiesByDate = jest.fn();
const mockPauseReminders = jest.fn();
const mockResumeReminders = jest.fn();

jest.mock('../store/useUserStore', () => ({
  useUserStore: () => ({
    userInfo: { weight: 70, initialWeight: 75, dailyTarget: 300 },
    fetchUserInfo: mockFetchUserInfo,
    updateWeight: mockUpdateWeight,
  }),
}));

jest.mock('../store/useStatsStore', () => ({
  useStatsStore: () => ({
    todayStats: { totalCalories: 0, targetCalories: 300, streak: 0 },
    historyStats: { totalCalories: 0, totalStreak: 0, totalAchieved: 0, weightChange: { initial: 75, current: 70, delta: -5 } },
    fetchTodayStats: mockFetchTodayStats,
    fetchHistoryStats: mockFetchHistoryStats,
  }),
}));

jest.mock('../store/useActivityStore', () => ({
  useActivityStore: () => ({
    todayActivities: [],
    fetchActivitiesByDate: mockFetchActivitiesByDate,
  }),
}));

jest.mock('../store/useSettingsStore', () => ({
  useSettingsStore: () => ({
    reminderStatus: { isPaused: false },
    pauseReminders: mockPauseReminders,
    resumeReminders: mockResumeReminders,
  }),
}));

jest.mock('../constants', () => ({
  COLORS: { PRIMARY: '#7C3AED', PRIMARY_LIGHT: '#A855F7', SUCCESS: '#22C55E', WARNING: '#F59E0B', INFO: '#3B82F6' },
}));

describe('Home page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('allows entering and saving weight from the home page', async () => {
    render(<Home />);

    const editButton = screen.getByText('更新');
    fireEvent.click(editButton);

    const input = screen.getByTestId('weight-input');
    fireEvent.change(input, { target: { value: '75' } });

    const saveButton = screen.getByText('保存');
    await act(async () => {
      fireEvent.click(saveButton);
    });

    expect(mockUpdateWeight).toHaveBeenCalledWith(75);
  });
});
