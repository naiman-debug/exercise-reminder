import { create } from 'zustand';
import { ReminderSettings, ReminderStatus } from '../types';

interface SettingsState {
  reminderSettings: ReminderSettings[];
  reminderStatus: ReminderStatus;
  autoStartEnabled: boolean;
  globalMinIntervalSec: number;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchReminderSettings: () => Promise<void>;
  updateReminderSettings: (settings: ReminderSettings) => Promise<void>;
  updateReminderSettingsBatch: (settings: ReminderSettings[]) => Promise<void>;
  fetchReminderStatus: () => Promise<void>;
  pauseReminders: () => Promise<void>;
  resumeReminders: () => Promise<void>;
  fetchAutoStartSetting: () => Promise<void>;
  setAutoStartEnabled: (enabled: boolean) => Promise<void>;
  fetchGlobalMinInterval: () => Promise<void>;
  setGlobalMinInterval: (seconds: number) => Promise<void>;
  resetSettings: () => Promise<void>;
  exportSettings: () => Promise<string>;
  clearError: () => void;
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  reminderSettings: [],
  reminderStatus: { isRunning: false, isPaused: false },
  autoStartEnabled: false,
  globalMinIntervalSec: 300,
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

  updateReminderSettingsBatch: async (settings) => {
    set({ isLoading: true, error: null });
    try {
      await Promise.all(settings.map((item) => window.electronAPI.updateReminderSettings(item)));
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

  fetchAutoStartSetting: async () => {
    set({ isLoading: true, error: null });
    try {
      const enabled = await window.electronAPI.getAutoStart();
      set({ autoStartEnabled: enabled, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  setAutoStartEnabled: async (enabled) => {
    set({ isLoading: true, error: null });
    try {
      const updated = await window.electronAPI.setAutoStart(enabled);
      set({ autoStartEnabled: updated, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  fetchGlobalMinInterval: async () => {
    set({ isLoading: true, error: null });
    try {
      const value = await window.electronAPI.getGlobalMinInterval();
      set({ globalMinIntervalSec: value, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  setGlobalMinInterval: async (seconds) => {
    set({ isLoading: true, error: null });
    try {
      const updated = await window.electronAPI.setGlobalMinInterval(seconds);
      set({ globalMinIntervalSec: updated, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  clearError: () => set({ error: null }),

  resetSettings: async () => {
    set({
      reminderSettings: [],
      reminderStatus: { isRunning: false, isPaused: false },
      autoStartEnabled: false,
      globalMinIntervalSec: 300,
      isLoading: false,
      error: null,
    });
  },

  exportSettings: async () => {
    const state = get();
    return JSON.stringify({
      reminderSettings: state.reminderSettings,
      reminderStatus: state.reminderStatus,
      autoStartEnabled: state.autoStartEnabled,
      globalMinIntervalSec: state.globalMinIntervalSec,
    });
  },
}));
