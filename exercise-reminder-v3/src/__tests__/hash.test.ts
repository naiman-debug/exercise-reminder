import { normalizeHash } from '../utils/hash';

describe('normalizeHash', () => {
  it('removes query string from hash route', () => {
    expect(normalizeHash('#/reminder?type=stand&duration=300')).toBe('#/reminder');
  });

  it('defaults to root when hash is empty', () => {
    expect(normalizeHash('')).toBe('#/');
    expect(normalizeHash(undefined)).toBe('#/');
    expect(normalizeHash(null)).toBe('#/');
  });
});
