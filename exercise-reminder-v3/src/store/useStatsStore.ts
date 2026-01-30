import { create } from 'zustand';
import { DailyStats, HistoryStats } from '../types';

interface StatsState {
  todayStats: DailyStats | null;
  historyStats: HistoryStats | null;
  streakDays: number;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchTodayStats: (date?: string) => Promise<void>;
  fetchHistoryStats: () => Promise<void>;
  fetchStreakDays: () => Promise<void>;
  clearError: () => void;
}

export const useStatsStore = create<StatsState>((set, get) => ({
  todayStats: null,
  historyStats: null,
  streakDays: 0,
  isLoading: false,
  error: null,

  fetchTodayStats: async (date) => {
    if (!date) {
      date = new Date().toISOString().split('T')[0];
    }
    set({ isLoading: true, error: null });
    try {
      const stats = await window.electronAPI.getTodayStats(date);
      set({ todayStats: stats, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  fetchHistoryStats: async () => {
    set({ isLoading: true, error: null });
    try {
      const stats = await window.electronAPI.getHistoryStats();
      set({ historyStats: stats, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  fetchStreakDays: async () => {
    try {
      const streak = await window.electronAPI.getStreakDays();
      set({ streakDays: streak });
    } catch (error) {
      set({ error: (error as Error).message });
    }
  },

  clearError: () => set({ error: null }),
}));
