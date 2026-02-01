import { act } from 'react';
import { render, screen } from '@testing-library/react';
import ReminderModal from '../pages/ReminderModal';

beforeEach(() => {
  (window as any).electronAPI = {
    saveActivity: jest.fn(),
    getUserInfo: jest.fn().mockResolvedValue({ weight: 70 }),
  };
});

describe('ReminderModal', () => {
  it('renders exercise modal with calories section', async () => {
    window.location.hash = '#/reminder?type=exercise&duration=120&exerciseName=开合跳&metValue=8';
    render(<ReminderModal />);
    await act(async () => {
      await Promise.resolve();
    });

    const modal = screen.getByTestId('reminder-modal');
    expect(modal).toBeInTheDocument();
    expect(modal).toHaveAttribute('data-variant', 'exercise');
    expect(screen.getByText('开合跳')).toBeInTheDocument();
    expect(screen.getByText('预计消耗：')).toBeInTheDocument();
  });

  it('switches countdown color to critical at 5 seconds', async () => {
    jest.useFakeTimers();
    window.location.hash = '#/reminder?type=gaze&duration=6';

    render(<ReminderModal />);
    await act(async () => {
      await Promise.resolve();
    });

    act(() => {
      jest.advanceTimersByTime(1000);
    });

    const countdown = screen.getByTestId('countdown-display');
    expect(countdown.className).toContain('critical');

    jest.useRealTimers();
  });

  it('saves activity with timestamp, date, calories and completed flag', async () => {
    jest.useFakeTimers();
    const saveActivity = jest.fn();
    (window as any).electronAPI = {
      saveActivity,
      getUserInfo: jest.fn().mockResolvedValue({ weight: 80 }),
    };

    window.location.hash = '#/reminder?type=exercise&duration=1&exerciseName=开合跳&metValue=8';
    render(<ReminderModal />);
    await act(async () => {
      await Promise.resolve();
    });

    act(() => {
      jest.advanceTimersByTime(1000);
    });

    expect(saveActivity).toHaveBeenCalledTimes(1);
    const payload = saveActivity.mock.calls[0][0];
    expect(payload).toMatchObject({
      type: 'exercise',
      name: '开合跳',
      duration: 1,
      metValue: 8,
      completed: true,
    });
    expect(typeof payload.timestamp).toBe('string');
    expect(typeof payload.date).toBe('string');
    expect(typeof payload.calories).toBe('number');

    jest.useRealTimers();
  });
});
