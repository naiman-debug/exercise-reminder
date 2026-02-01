import { renderHook, act, waitFor } from '@testing-library/react';
import { useSettingsStore } from '../store/useSettingsStore';

describe('useSettingsStore', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    // Reset store state
    useSettingsStore.setState({
      reminderSettings: [],
      reminderStatus: { isRunning: false, isPaused: false },
      isLoading: false,
      error: null,
      autoStartEnabled: false,
      globalMinIntervalSec: 300,
    });
  });

  describe('fetchReminderSettings', () => {
    it('should fetch reminder settings successfully', async () => {
      const mockSettings = [
        { id: 1, type: 'exercise' as const, intervalMin: 10, intervalMax: 20, duration: 120, enabled: true, updatedAt: '2024-01-01' },
        { id: 2, type: 'gaze' as const, intervalMin: 10, intervalMax: 20, duration: 60, enabled: true, updatedAt: '2024-01-01' },
        { id: 3, type: 'stand' as const, intervalMin: 10, intervalMax: 20, duration: 300, enabled: true, updatedAt: '2024-01-01' },
      ];

      (globalThis.electronAPI.getReminderSettings as jest.Mock).mockResolvedValue(mockSettings);

      const { result } = renderHook(() => useSettingsStore());

      await act(async () => {
        await result.current.fetchReminderSettings();
      });

      expect(result.current.reminderSettings).toEqual(mockSettings);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe(null);
    });

    it('should handle fetch error', async () => {
      const mockError = new Error('Failed to fetch settings');
      (globalThis.electronAPI.getReminderSettings as jest.Mock).mockRejectedValue(mockError);

      const { result } = renderHook(() => useSettingsStore());

      await act(async () => {
        await result.current.fetchReminderSettings();
      });

      expect(result.current.reminderSettings).toEqual([]);
      expect(result.current.error).toBe(mockError.message);
    });
  });

  describe('updateReminderSettings', () => {
    it('should update reminder settings and refetch', async () => {
      const mockSettings = [
        { id: 1, type: 'exercise' as const, intervalMin: 15, intervalMax: 25, duration: 150, enabled: true, updatedAt: '2024-01-01' },
      ];

      (globalThis.electronAPI.updateReminderSettings as jest.Mock).mockResolvedValue({ success: true });
      (globalThis.electronAPI.getReminderSettings as jest.Mock).mockResolvedValue(mockSettings);

      const { result } = renderHook(() => useSettingsStore());

      await act(async () => {
        await result.current.updateReminderSettings(mockSettings[0]);
      });

      expect(globalThis.electronAPI.updateReminderSettings).toHaveBeenCalledWith(mockSettings[0]);
      expect(result.current.reminderSettings).toEqual(mockSettings);
    });
  });

  describe('autoStart settings', () => {
    it('should fetch auto-start setting', async () => {
      (globalThis.electronAPI.getAutoStart as jest.Mock).mockResolvedValue(true);
      const { result } = renderHook(() => useSettingsStore());

      await act(async () => {
        await result.current.fetchAutoStartSetting();
      });

      expect(globalThis.electronAPI.getAutoStart).toHaveBeenCalled();
      expect(result.current.autoStartEnabled).toBe(true);
    });

    it('should set auto-start setting', async () => {
      (globalThis.electronAPI.setAutoStart as jest.Mock).mockResolvedValue(true);
      const { result } = renderHook(() => useSettingsStore());

      await act(async () => {
        await result.current.setAutoStartEnabled(true);
      });

      expect(globalThis.electronAPI.setAutoStart).toHaveBeenCalledWith(true);
      expect(result.current.autoStartEnabled).toBe(true);
    });
  });

  describe('global min interval settings', () => {
    it('should fetch global min interval', async () => {
      (globalThis.electronAPI.getGlobalMinInterval as jest.Mock).mockResolvedValue(240);
      const { result } = renderHook(() => useSettingsStore());

      await act(async () => {
        await result.current.fetchGlobalMinInterval();
      });

      expect(globalThis.electronAPI.getGlobalMinInterval).toHaveBeenCalled();
      expect(result.current.globalMinIntervalSec).toBe(240);
    });

    it('should set global min interval', async () => {
      (globalThis.electronAPI.setGlobalMinInterval as jest.Mock).mockResolvedValue(300);
      const { result } = renderHook(() => useSettingsStore());

      await act(async () => {
        await result.current.setGlobalMinInterval(300);
      });

      expect(globalThis.electronAPI.setGlobalMinInterval).toHaveBeenCalledWith(300);
      expect(result.current.globalMinIntervalSec).toBe(300);
    });
  });

  describe('updateReminderSettingsBatch', () => {
    it('should batch update reminder settings and refetch once', async () => {
      const mockSettings = [
        { id: 1, type: 'exercise' as const, intervalMin: 10, intervalMax: 20, duration: 120, enabled: true, updatedAt: '2024-01-01' },
        { id: 2, type: 'gaze' as const, intervalMin: 10, intervalMax: 20, duration: 60, enabled: true, updatedAt: '2024-01-01' },
      ];

      (globalThis.electronAPI.updateReminderSettings as jest.Mock).mockResolvedValue({ success: true });
      (globalThis.electronAPI.getReminderSettings as jest.Mock).mockResolvedValue(mockSettings);

      const { result } = renderHook(() => useSettingsStore());

      await act(async () => {
        await result.current.updateReminderSettingsBatch(mockSettings);
      });

      expect(globalThis.electronAPI.updateReminderSettings).toHaveBeenCalledTimes(2);
      expect(globalThis.electronAPI.getReminderSettings).toHaveBeenCalledTimes(1);
      expect(result.current.reminderSettings).toEqual(mockSettings);
    });
  });

  describe('resetSettings', () => {
    it('should reset all settings to default values', async () => {
      const { result } = renderHook(() => useSettingsStore());

      // Verify resetSettings method exists
      expect(typeof result.current.resetSettings).toBe('function');

      // Reset settings
      await act(async () => {
        await result.current.resetSettings();
      });

      // Verify all values are reset to defaults
      expect(result.current.reminderSettings).toEqual([]);
      expect(result.current.reminderStatus).toEqual({ isRunning: false, isPaused: false });
      expect(result.current.autoStartEnabled).toBe(false);
      expect(result.current.globalMinIntervalSec).toBe(300);
      expect(result.current.error).toBe(null);
      expect(result.current.isLoading).toBe(false);
    });
  });

  describe('exportSettings', () => {
    it('should export settings as JSON string', async () => {
      const { result } = renderHook(() => useSettingsStore());

      // Verify exportSettings method exists
      expect(typeof result.current.exportSettings).toBe('function');

      // Set some settings
      useSettingsStore.setState({
        reminderSettings: [
          { id: 1, type: 'exercise' as const, intervalMin: 10, intervalMax: 20, duration: 120, enabled: true, updatedAt: '2024-01-01' },
        ],
        autoStartEnabled: true,
        globalMinIntervalSec: 600,
      });

      // Export settings
      let exportedJson: string = '';
      await act(async () => {
        exportedJson = await result.current.exportSettings();
      });

      // Verify exported JSON contains the settings
      const exported = JSON.parse(exportedJson);
      expect(exported.reminderSettings).toHaveLength(1);
      expect(exported.autoStartEnabled).toBe(true);
      expect(exported.globalMinIntervalSec).toBe(600);
    });

    it('should export default settings when empty', async () => {
      const { result } = renderHook(() => useSettingsStore());

      let exportedJson: string = '';
      await act(async () => {
        exportedJson = await result.current.exportSettings();
      });

      const exported = JSON.parse(exportedJson);
      expect(exported.reminderSettings).toEqual([]);
      expect(exported.autoStartEnabled).toBe(false);
      expect(exported.globalMinIntervalSec).toBe(300);
    });
  });
});
