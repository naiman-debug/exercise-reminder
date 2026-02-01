export const normalizeHash = (hash: string | null | undefined): string => {
  const value = hash && hash.length > 0 ? hash : '#/';
  const normalized = value.split('?')[0];
  return normalized && normalized.length > 0 ? normalized : '#/';
};
