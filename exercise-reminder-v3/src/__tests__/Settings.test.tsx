import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Settings from '../pages/Settings';

const mockFetchReminderSettings = jest.fn();
const mockUpdateReminderSettingsBatch = jest.fn();
const mockFetchAutoStartSetting = jest.fn();
const mockSetAutoStartEnabled = jest.fn();
const mockFetchGlobalMinInterval = jest.fn();
const mockSetGlobalMinInterval = jest.fn();
const mockReminderSettings = [
  { id: 1, type: 'exercise', intervalMin: 10, intervalMax: 20, duration: 120, enabled: true, updatedAt: '2024-01-01' },
  { id: 2, type: 'gaze', intervalMin: 10, intervalMax: 20, duration: 60, enabled: true, updatedAt: '2024-01-01' },
  { id: 3, type: 'stand', intervalMin: 10, intervalMax: 20, duration: 300, enabled: true, updatedAt: '2024-01-01' },
];

jest.mock('../store/useSettingsStore', () => ({
  useSettingsStore: () => ({
    reminderSettings: mockReminderSettings,
    fetchReminderSettings: mockFetchReminderSettings,
    updateReminderSettingsBatch: mockUpdateReminderSettingsBatch,
    fetchAutoStartSetting: mockFetchAutoStartSetting,
    setAutoStartEnabled: mockSetAutoStartEnabled,
    autoStartEnabled: false,
    globalMinIntervalSec: 300,
    fetchGlobalMinInterval: mockFetchGlobalMinInterval,
    setGlobalMinInterval: mockSetGlobalMinInterval,
  }),
}));

jest.mock('../store/useUserStore', () => ({
  useUserStore: () => ({
    userInfo: null,
    saveUserInfo: jest.fn(),
    fetchUserInfo: jest.fn(),
  }),
}));

jest.mock('../store/useExerciseStore', () => ({
  useExerciseStore: () => ({
    exercises: [],
    fetchAllExercises: jest.fn(),
    addExercise: jest.fn(),
    deleteExercise: jest.fn(),
  }),
}));

jest.mock('../constants', () => ({
  DEFAULTS: { HEIGHT: 170, WEIGHT: 70, AGE: 30, DAILY_TARGET: 300 },
  GENDER: { MALE: 'male', FEMALE: 'female' },
  COLORS: { PRIMARY: '#7C3AED', HIGH_INTENSITY: '#EF4444', MEDIUM_INTENSITY: '#F97316', LOW_INTENSITY: '#22C55E', INFO: '#3B82F6' },
  INTENSITY_LEVELS: { HIGH: 'high', MEDIUM: 'medium', LOW: 'low' },
}));

describe('Settings page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  afterEach(() => {
    (window.alert as jest.Mock).mockRestore();
  });

  it('saves all reminder settings via footer button', async () => {
    render(<Settings />);

    const reminderTab = screen.getByTestId('tab-reminder');
    fireEvent.click(reminderTab);

    const saveButton = await screen.findByTestId('footer-save');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(mockUpdateReminderSettingsBatch).toHaveBeenCalledTimes(1);
    });
  });

  it('shows a save message without blocking tab navigation', async () => {
    render(<Settings />);

    const saveButton = await screen.findByTestId('footer-save');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByTestId('status-toast')).toHaveTextContent('已保存');
    });

    const reminderTab = screen.getByTestId('tab-reminder');
    fireEvent.click(reminderTab);

    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('提醒设置');
  });

  it('auto-corrects reminder interval when min is greater than max on save', async () => {
    render(<Settings />);

    const reminderTab = screen.getByTestId('tab-reminder');
    fireEvent.click(reminderTab);

    const intervalMinInput = screen.getByTestId('interval-min-exercise');
    const intervalMaxInput = screen.getByTestId('interval-max-exercise');

    fireEvent.change(intervalMinInput, { target: { value: '30' } });

    const saveButton = await screen.findByTestId('footer-save');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(intervalMinInput).toHaveValue(20);
      expect(intervalMaxInput).toHaveValue(30);
    });
  });

  it('saves global minimum interval when saving reminder settings', async () => {
    render(<Settings />);

    const reminderTab = screen.getByTestId('tab-reminder');
    fireEvent.click(reminderTab);

    const intervalInput = screen.getByTestId('global-min-interval');
    fireEvent.change(intervalInput, { target: { value: '240' } });

    const saveButton = await screen.findByTestId('footer-save');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(mockSetGlobalMinInterval).toHaveBeenCalledWith(240);
    });
  });

  it('toggles auto-start setting', async () => {
    render(<Settings />);

    const exerciseTab = screen.getByTestId('tab-exercise');
    fireEvent.click(exerciseTab);

    const toggle = await screen.findByTestId('auto-start-toggle');
    fireEvent.click(toggle);

    await waitFor(() => {
      expect(mockSetAutoStartEnabled).toHaveBeenCalledWith(true);
    });
  });
});
