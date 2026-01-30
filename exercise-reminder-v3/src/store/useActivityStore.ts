import { create } from 'zustand';
import { Activity } from '../types';

interface ActivityState {
  activities: Activity[];
  todayActivities: Activity[];
  isLoading: boolean;
  error: string | null;

  // Actions
  saveActivity: (activity: Omit<Activity, 'id' | 'timestamp' | 'date' | 'completed'>) => Promise<void>;
  fetchActivitiesByDate: (date: string) => Promise<void>;
  fetchRecentActivities: (limit?: number) => Promise<void>;
  clearError: () => void;
}

export const useActivityStore = create<ActivityState>((set, get) => ({
  activities: [],
  todayActivities: [],
  isLoading: false,
  error: null,

  saveActivity: async (activity) => {
    set({ isLoading: true, error: null });
    try {
      const now = new Date();
      const date = now.toISOString().split('T')[0];
      const timestamp = now.toISOString();

      const activityWithMeta = {
        ...activity,
        timestamp,
        date,
        completed: true,
      };

      await window.electronAPI.saveActivity(activityWithMeta);

      // 重新获取今日活动
      await get().fetchActivitiesByDate(date);

      set({ isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  fetchActivitiesByDate: async (date) => {
    set({ isLoading: true, error: null });
    try {
      const activities = await window.electronAPI.getActivitiesByDate(date);
      set({ todayActivities: activities, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  fetchRecentActivities: async (limit = 50) => {
    set({ isLoading: true, error: null });
    try {
      const activities = await window.electronAPI.getRecentActivities(limit);
      set({ activities, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  clearError: () => set({ error: null }),
}));
