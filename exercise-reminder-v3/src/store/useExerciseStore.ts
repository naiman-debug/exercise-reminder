import { create } from 'zustand';
import { Exercise } from '../types';

interface ExerciseState {
  exercises: Exercise[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchAllExercises: () => Promise<void>;
  addExercise: (exercise: Omit<Exercise, 'id' | 'createdAt'>) => Promise<void>;
  deleteExercise: (id: number) => Promise<void>;
  clearError: () => void;
}

export const useExerciseStore = create<ExerciseState>((set, get) => ({
  exercises: [],
  isLoading: false,
  error: null,

  fetchAllExercises: async () => {
    set({ isLoading: true, error: null });
    try {
      const exercises = await window.electronAPI.getAllExercises();
      set({ exercises, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  addExercise: async (exercise) => {
    set({ isLoading: true, error: null });
    try {
      await window.electronAPI.addExercise(exercise);

      // 重新获取运动列表
      const exercises = await window.electronAPI.getAllExercises();
      set({ exercises, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  deleteExercise: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await window.electronAPI.deleteExercise(id);

      // 重新获取运动列表
      const exercises = await window.electronAPI.getAllExercises();
      set({ exercises, isLoading: false });
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false });
    }
  },

  clearError: () => set({ error: null }),
}));
