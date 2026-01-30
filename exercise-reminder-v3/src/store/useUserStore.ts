import { create } from 'zustand';
import { UserInfo } from '../types';

interface UserState {
  userInfo: UserInfo | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchUserInfo: () => Promise<void>;
  saveUserInfo: (info: Omit<UserInfo, 'id' | 'createdAt' | 'updatedAt'>) => Promise<void>;
  updateWeight: (weight: number) => Promise<void>;
  clearError: () => void;
}

export const useUserStore = create<UserState>((set, get) => ({
  userInfo: null,
  isLoading: false,
  error: null,

  fetchUserInfo: async () => {
    set({ isLoading: true, error: null });
    try {
      const info = await window.electronAPI.getUserInfo();
      set({ userInfo: info, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  saveUserInfo: async (info) => {
    set({ isLoading: true, error: null });
    try {
      await window.electronAPI.saveUserInfo(info);
      // 重新获取用户信息
      const updatedInfo = await window.electronAPI.getUserInfo();
      set({ userInfo: updatedInfo, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  updateWeight: async (weight) => {
    set({ isLoading: true, error: null });
    try {
      await window.electronAPI.updateWeight(weight);
      // 重新获取用户信息
      const updatedInfo = await window.electronAPI.getUserInfo();
      set({ userInfo: updatedInfo, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  clearError: () => set({ error: null }),
}));
