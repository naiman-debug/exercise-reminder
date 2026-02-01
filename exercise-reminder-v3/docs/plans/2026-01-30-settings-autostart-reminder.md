# Settings Global Save & Autostart Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make Settings page match prototype by adding global reminder save and a real system autostart toggle.

**Architecture:** Frontend keeps draft reminder settings and saves all at once; Electron main process exposes autostart IPC that writes system login item and persists a system_settings key.

**Tech Stack:** React, Zustand, Electron IPC, better-sqlite3, Jest/RTL.

---

### Task 1: Add tests for new Settings store behaviors (TDD - RED)

**Files:**
- Modify: `src/__tests__/useSettingsStore.test.ts`
- Modify: `jest.setup.js` (add new electronAPI mocks)

**Step 1: Write failing tests**
Add tests for:
- `fetchAutoStartSetting` sets `autoStartEnabled` from `electronAPI.getAutoStart`.
- `setAutoStartEnabled` calls `electronAPI.setAutoStart` and updates state.
- `updateReminderSettingsBatch` calls `electronAPI.updateReminderSettings` for each setting and refetches once.

```typescript
// new tests to add in src/__tests__/useSettingsStore.test.ts
it('should fetch auto-start setting', async () => {
  (global.electronAPI.getAutoStart as jest.Mock).mockResolvedValue(true);
  const { result } = renderHook(() => useSettingsStore());

  await act(async () => {
    await result.current.fetchAutoStartSetting();
  });

  expect(global.electronAPI.getAutoStart).toHaveBeenCalled();
  expect(result.current.autoStartEnabled).toBe(true);
});

it('should set auto-start setting', async () => {
  (global.electronAPI.setAutoStart as jest.Mock).mockResolvedValue(true);
  const { result } = renderHook(() => useSettingsStore());

  await act(async () => {
    await result.current.setAutoStartEnabled(true);
  });

  expect(global.electronAPI.setAutoStart).toHaveBeenCalledWith(true);
  expect(result.current.autoStartEnabled).toBe(true);
});

it('should batch update reminder settings and refetch once', async () => {
  const mockSettings = [
    { id: 1, type: 'exercise' as const, intervalMin: 10, intervalMax: 20, duration: 120, enabled: true, updatedAt: '2024-01-01' },
    { id: 2, type: 'gaze' as const, intervalMin: 10, intervalMax: 20, duration: 60, enabled: true, updatedAt: '2024-01-01' },
  ];

  (global.electronAPI.updateReminderSettings as jest.Mock).mockResolvedValue({ success: true });
  (global.electronAPI.getReminderSettings as jest.Mock).mockResolvedValue(mockSettings);

  const { result } = renderHook(() => useSettingsStore());

  await act(async () => {
    await result.current.updateReminderSettingsBatch(mockSettings);
  });

  expect(global.electronAPI.updateReminderSettings).toHaveBeenCalledTimes(2);
  expect(global.electronAPI.getReminderSettings).toHaveBeenCalledTimes(1);
  expect(result.current.reminderSettings).toEqual(mockSettings);
});
```

Also extend `jest.setup.js` with:
```javascript
getAutoStart: jest.fn(),
setAutoStart: jest.fn(),
```

**Step 2: Run tests to verify failure**
Run: `npm test -- src/__tests__/useSettingsStore.test.ts`
Expected: FAIL with missing methods on store/electronAPI.

---

### Task 2: Implement Settings store autostart + batch update (TDD - GREEN)

**Files:**
- Modify: `src/store/useSettingsStore.ts`
- Modify: `src/global.d.ts`

**Step 1: Add store state + actions**
Update store interface and implementation:
- `autoStartEnabled: boolean`
- `fetchAutoStartSetting: () => Promise<void>`
- `setAutoStartEnabled: (enabled: boolean) => Promise<void>`
- `updateReminderSettingsBatch: (settings: ReminderSettings[]) => Promise<void>`

Example implementation outline:
```typescript
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
updateReminderSettingsBatch: async (settings) => {
  set({ isLoading: true, error: null });
  try {
    await Promise.all(settings.map(item => window.electronAPI.updateReminderSettings(item)));
    const updated = await window.electronAPI.getReminderSettings();
    set({ reminderSettings: updated, isLoading: false });
  } catch (error) {
    set({ error: (error as Error).message, isLoading: false });
  }
},
```

Update `src/global.d.ts` to add:
```typescript
getAutoStart: () => Promise<boolean>;
setAutoStart: (enabled: boolean) => Promise<boolean>;
```

**Step 2: Run tests to verify pass**
Run: `npm test -- src/__tests__/useSettingsStore.test.ts`
Expected: PASS.

---

### Task 3: Add IPC and preload for autostart (TDD - RED)

**Files:**
- Modify: `electron/ipc/channels.ts`
- Modify: `electron/ipc/handlers.ts`
- Modify: `electron/preload.ts`
- Modify: `src/global.d.ts` (if not yet done)

**Step 1: Write failing test**
Create a new test file `electron/__tests__/autostart.test.ts` (or `src/__tests__/autostart-ipc.test.ts`) that mocks Electron `app` and asserts:
- `getAutoStart` returns boolean
- `setAutoStart(true)` calls `app.setLoginItemSettings({ openAtLogin: true })` and persists `system_settings`

If no test harness exists for electron, note this and confirm with you whether to skip IPC unit tests (project does not currently test main process). If skipping, explicitly document why in work log.

**Step 2: Run test to see failure**
Run: `npm test -- electron/__tests__/autostart.test.ts`
Expected: FAIL until handlers/preload added.

---

### Task 4: Implement IPC handlers + preload methods (TDD - GREEN)

**Files:**
- Modify: `electron/ipc/channels.ts`
- Modify: `electron/ipc/handlers.ts`
- Modify: `electron/preload.ts`

**Step 1: Add channels**
Add:
```typescript
GET_AUTO_START: 'get-auto-start',
SET_AUTO_START: 'set-auto-start',
```

**Step 2: Implement handlers**
In `electron/ipc/handlers.ts`, import `app` and add:
```typescript
ipcMain.handle(IPC_CHANNELS.GET_AUTO_START, () => {
  const login = app.getLoginItemSettings();
  const stored = queries.getSystemSetting('auto_start_enabled');
  if (stored === null) {
    queries.setSystemSetting('auto_start_enabled', login.openAtLogin ? 'true' : 'false');
  }
  return login.openAtLogin;
});

ipcMain.handle(IPC_CHANNELS.SET_AUTO_START, (_, enabled: boolean) => {
  app.setLoginItemSettings({ openAtLogin: enabled });
  queries.setSystemSetting('auto_start_enabled', enabled ? 'true' : 'false');
  return enabled;
});
```

**Step 3: Expose preload methods**
Add to `electron/preload.ts`:
```typescript
getAutoStart: () => ipcRenderer.invoke(IPC_CHANNELS.GET_AUTO_START),
setAutoStart: (enabled) => ipcRenderer.invoke(IPC_CHANNELS.SET_AUTO_START, enabled),
```
And extend `ElectronAPI` interface accordingly.

**Step 4: Run IPC tests** (if created)
Run: `npm test -- electron/__tests__/autostart.test.ts`
Expected: PASS.

---

### Task 5: Update Settings UI for global save + autostart toggle (TDD - RED)

**Files:**
- Modify: `src/pages/Settings.tsx`
- Create: `src/__tests__/Settings.test.tsx`

**Step 1: Write failing UI test**
Test that:
- Clicking footer “保存设置” calls `updateReminderSettingsBatch` with current draft settings.
- Toggling “开机自启动” calls `setAutoStartEnabled`.

Example (outline):
```typescript
// Settings.test.tsx
it('saves all reminder settings via footer button', async () => {
  // mock store methods, render Settings, click button, assert call
});

it('toggles auto-start setting', async () => {
  // render Settings with exercise tab active, click toggle, assert call
});
```

**Step 2: Run tests to verify failure**
Run: `npm test -- src/__tests__/Settings.test.tsx`
Expected: FAIL until UI updated.

---

### Task 6: Implement Settings UI changes (TDD - GREEN)

**Files:**
- Modify: `src/pages/Settings.tsx`

**Step 1: Global save**
- Remove per-card “确认” button in reminder settings tab.
- Add footer “保存设置” handler:
```typescript
const handleSaveAllReminderSettings = async () => {
  await updateReminderSettingsBatch(draftSettings);
  alert('提醒设置已保存');
};
```
- Hook to page footer button (currently exists for profile save, adjust as needed).

**Step 2: Autostart toggle**
- Add `autoStartEnabled`, `fetchAutoStartSetting`, `setAutoStartEnabled` from store.
- Fetch on mount (same effect as reminder settings).
- Render toggle in exercise tab (align with prototype):
```tsx
<input
  type="checkbox"
  checked={autoStartEnabled}
  onChange={async (e) => {
    const next = e.target.checked;
    await setAutoStartEnabled(next);
  }}
/>
```
- On error, revert UI state and show alert.

**Step 3: Run UI tests**
Run: `npm test -- src/__tests__/Settings.test.tsx`
Expected: PASS.

---

### Task 7: Full test run + documentation

**Step 1: Run full test suite**
Run: `npm test`
Expected: PASS

**Step 2: Update work log**
Update `docs/WORK-LOG.md` with:
- completed tasks
- files changed
- issues + fixes
- next steps
- progress table

**Step 3: Request code review**
Use `requesting-code-review` skill after changes are complete and tests pass.

---

## Notes / Open Questions
- If there is no Electron test harness, confirm whether to skip IPC unit tests and document reason.
