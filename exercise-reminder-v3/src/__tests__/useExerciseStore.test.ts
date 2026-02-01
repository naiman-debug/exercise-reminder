import { renderHook, act } from '@testing-library/react';
import { useExerciseStore } from '../store/useExerciseStore';

describe('useExerciseStore', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    useExerciseStore.setState({
      exercises: [],
      isLoading: false,
      error: null,
    });
  });

  describe('fetchAllExercises', () => {
    it('should fetch all exercises successfully', async () => {
      const mockExercises = [
        { id: 1, name: '开合跳', metValue: 8.0, intensity: 'high' as const, createdAt: '2024-01-01' },
        { id: 2, name: '深蹲', metValue: 5.0, intensity: 'medium' as const, createdAt: '2024-01-01' },
      ];

      (globalThis.electronAPI.getAllExercises as jest.Mock).mockResolvedValue(mockExercises);

      const { result } = renderHook(() => useExerciseStore());

      await act(async () => {
        await result.current.fetchAllExercises();
      });

      expect(result.current.exercises).toEqual(mockExercises);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBe(null);
    });

    it('should handle fetch error', async () => {
      const mockError = new Error('Failed to fetch exercises');
      (globalThis.electronAPI.getAllExercises as jest.Mock).mockRejectedValue(mockError);

      const { result } = renderHook(() => useExerciseStore());

      await act(async () => {
        await result.current.fetchAllExercises();
      });

      expect(result.current.exercises).toEqual([]);
      expect(result.current.error).toBe(mockError.message);
    });
  });

  describe('addExercise', () => {
    it('should add exercise and refetch list', async () => {
      const newExercise = { name: '俯卧撑', metValue: 8.0, intensity: 'high' as const };
      const updatedExercises = [
        { id: 1, name: '开合跳', metValue: 8.0, intensity: 'high' as const, createdAt: '2024-01-01' },
        { id: 2, name: '俯卧撑', metValue: 8.0, intensity: 'high' as const, createdAt: '2024-01-01' },
      ];

      (globalThis.electronAPI.addExercise as jest.Mock).mockResolvedValue({ success: true });
      (globalThis.electronAPI.getAllExercises as jest.Mock).mockResolvedValue(updatedExercises);

      const { result } = renderHook(() => useExerciseStore());

      await act(async () => {
        await result.current.addExercise(newExercise);
      });

      expect(globalThis.electronAPI.addExercise).toHaveBeenCalledWith(newExercise);
      expect(result.current.exercises).toEqual(updatedExercises);
    });
  });

  describe('deleteExercise', () => {
    it('should delete exercise and refetch list', async () => {
      const updatedExercises = [
        { id: 1, name: '开合跳', metValue: 8.0, intensity: 'high' as const, createdAt: '2024-01-01' },
      ];

      (globalThis.electronAPI.deleteExercise as jest.Mock).mockResolvedValue({ success: true });
      (globalThis.electronAPI.getAllExercises as jest.Mock).mockResolvedValue(updatedExercises);

      const { result } = renderHook(() => useExerciseStore());

      await act(async () => {
        await result.current.deleteExercise(2);
      });

      expect(globalThis.electronAPI.deleteExercise).toHaveBeenCalledWith(2);
      expect(result.current.exercises).toEqual(updatedExercises);
    });
  });
});
