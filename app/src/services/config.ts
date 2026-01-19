// app/src/services/config.ts

export interface AppConfig {
  anthropicApiKey: string | null;
  webSearchApiKey: string | null;
  webSearchApiUrl: string | null;
}

const CONFIG_KEY = 'orgtransformation-config';

export function getConfig(): AppConfig {
  const stored = localStorage.getItem(CONFIG_KEY);
  if (stored) {
    return JSON.parse(stored);
  }
  return {
    anthropicApiKey: null,
    webSearchApiKey: null,
    webSearchApiUrl: null,
  };
}

export function setConfig(config: Partial<AppConfig>): void {
  const current = getConfig();
  const updated = { ...current, ...config };
  localStorage.setItem(CONFIG_KEY, JSON.stringify(updated));
}

export function hasRequiredConfig(): boolean {
  const config = getConfig();
  return !!config.anthropicApiKey;
}
