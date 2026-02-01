import { IPC_CHANNELS } from '../ipc/channels';
import { registerIPCHandlers } from '../ipc/handlers';
import { ipcMain, app } from 'electron';

const handlers: Record<string, (...args: any[]) => any> = {};

jest.mock('electron', () => ({
  ipcMain: {
    handle: jest.fn((channel: string, handler: (...args: any[]) => any) => {
      handlers[channel] = handler;
    }),
  },
  app: {
    getLoginItemSettings: jest.fn(),
    setLoginItemSettings: jest.fn(),
  },
  BrowserWindow: {
    getAllWindows: jest.fn(() => []),
  },
}));

jest.mock('../database/db', () => ({
  getDatabase: jest.fn(() => ({})),
}));

const mockQueries = {
  getSystemSetting: jest.fn(),
  setSystemSetting: jest.fn(),
};

jest.mock('../database/queries', () => ({
  DatabaseQueries: jest.fn().mockImplementation(() => mockQueries),
}));

describe('autostart IPC handlers', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    Object.keys(handlers).forEach((key) => delete handlers[key]);
  });

  it('returns current auto-start state', async () => {
    (app.getLoginItemSettings as jest.Mock).mockReturnValue({ openAtLogin: true });
    (mockQueries.getSystemSetting as jest.Mock).mockReturnValue('true');

    registerIPCHandlers();

    const handler = handlers[IPC_CHANNELS.GET_AUTO_START];
    const result = await handler();

    expect(result).toBe(true);
    expect(app.getLoginItemSettings).toHaveBeenCalled();
  });

  it('sets auto-start state and persists setting', async () => {
    registerIPCHandlers();

    const handler = handlers[IPC_CHANNELS.SET_AUTO_START];
    const result = await handler(undefined, true);

    expect(app.setLoginItemSettings).toHaveBeenCalledWith({ openAtLogin: true });
    expect(mockQueries.setSystemSetting).toHaveBeenCalledWith('auto_start_enabled', 'true');
    expect(result).toBe(true);
  });
});
