import { create } from 'zustand';
import { ReminderSettings, ReminderStatus } from '../types';

interface SettingsState {
  reminderSettings: ReminderSettings[];
  reminderStatus: ReminderStatus;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchReminderSettings: () => Promise<void>;
  updateReminderSettings: (settings: ReminderSettings) => Promise<void>;
  fetchReminderStatus: () => Promise<void>;
  pauseReminders: () => Promise<void>;
  resumeReminders: () => Promise<void>;
  clearError: () => void;
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  reminderSettings: [],
  reminderStatus: { isRunning: false, isPaused: false },
  isLoading: false,
  error: null,

  fetchReminderSettings: async () => {
    set({ isLoading: true, error: null });
    try {
      const settings = await window.electronAPI.getReminderSettings();
      set({ reminderSettings: settings, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  updateReminderSettings: async (settings) => {
    set({ isLoading: true, error: null });
    try {
      await window.electronAPI.updateReminderSettings(settings);

      // 重新获取设置
      const updatedSettings = await window.electronAPI.getReminderSettings();
      set({ reminderSettings: updatedSettings, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  fetchReminderStatus: async () => {
    try {
      const status = await window.electronAPI.getReminderStatus();
      set({ reminderStatus: status });
    } catch (error) {
      set({ error: (error as Error).message });
    }
  },

  pauseReminders: async () => {
    try {
      await window.electronAPI.pauseReminders();
      set({ reminderStatus: { ...get().reminderStatus, isPaused: true } });
    } catch (error) {
      set({ error: (error as Error).message });
    }
  },

  resumeReminders: async () => {
    try {
      await window.electronAPI.resumeReminders();
      set({ reminderStatus: { ...get().reminderStatus, isPaused: false } });
    } catch (error) {
      set({ error: (error as Error).message });
    }
  },

  clearError: () => set({ error: null }),
}));
