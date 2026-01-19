// app/src/components/SettingsPanel.tsx
import { useState, useMemo } from 'react';
import { getConfig, setConfig, type AppConfig } from '../services/config';

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function SettingsPanel({ isOpen, onClose }: SettingsPanelProps) {
  // Re-initialize config from storage when modal opens
  const initialConfig = useMemo(
    () =>
      isOpen
        ? getConfig()
        : { anthropicApiKey: null, webSearchApiKey: null, webSearchApiUrl: null },
    [isOpen]
  );
  const [localConfig, setLocalConfig] = useState<AppConfig>(initialConfig);
  const [saved, setSaved] = useState(false);

  // Reset saved state when opening
  if (isOpen && saved) {
    setSaved(false);
  }

  const handleSave = () => {
    setConfig(localConfig);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">Settings</h2>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-600 rounded">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Anthropic API Key</label>
            <input
              type="password"
              value={localConfig.anthropicApiKey || ''}
              onChange={(e) => setLocalConfig({ ...localConfig, anthropicApiKey: e.target.value })}
              placeholder="sk-ant-..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <p className="text-xs text-gray-500 mt-1">Required for AI-powered conversations</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Web Search API URL (Optional)
            </label>
            <input
              type="text"
              value={localConfig.webSearchApiUrl || ''}
              onChange={(e) => setLocalConfig({ ...localConfig, webSearchApiUrl: e.target.value })}
              placeholder="https://api.example.com/search"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Web Search API Key (Optional)
            </label>
            <input
              type="password"
              value={localConfig.webSearchApiKey || ''}
              onChange={(e) => setLocalConfig({ ...localConfig, webSearchApiKey: e.target.value })}
              placeholder="Your API key"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <p className="text-xs text-gray-500 mt-1">Enables web search fallback for unknown questions</p>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-between">
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
          >
            Save Settings
          </button>
          {saved && <span className="text-sm text-green-600">Saved!</span>}
        </div>
      </div>
    </div>
  );
}
