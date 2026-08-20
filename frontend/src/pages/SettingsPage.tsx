import React, { useState, useEffect } from 'react';
import { Settings, Shield, Key, Eye, EyeOff, Save, CheckCircle2 } from 'lucide-react';
import { settingsService } from '../services/settingsService';
import { SettingsData } from '../types';
import { useToast } from '../context/ToastContext';

export const SettingsPage: React.FC = () => {
  const { showToast } = useToast();
  const [settings, setSettings] = useState<SettingsData | null>(null);
  const [provider, setProvider] = useState('smart_fallback');
  const [model, setModel] = useState('gpt-4o');
  const [apiKey, setApiKey] = useState('');
  const [githubToken, setGithubToken] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const [minConfidence, setMinConfidence] = useState(0.60);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const data = await settingsService.getSettings();
      setSettings(data);
      setProvider(data.llm_provider);
      setModel(data.llm_model);
      setMinConfidence(data.min_confidence);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const updated = await settingsService.updateSettings({
        llm_provider: provider,
        llm_model: model,
        llm_api_key: apiKey ? apiKey : undefined,
        github_token: githubToken ? githubToken : undefined,
        min_confidence: minConfidence
      });
      setSettings(updated);
      setApiKey('');
      setGithubToken('');
      showToast('success', 'Settings saved', 'Configuration updated successfully.');
    } catch (err) {
      showToast('error', 'Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="border-b border-surface-border pb-3">
        <h1 className="text-2xl font-bold text-text-primary">System Settings & Configuration</h1>
        <p className="text-xs text-text-secondary mt-0.5">Manage AI reasoning models, API keys, GitHub authentication, and review preferences.</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* LLM Configuration */}
        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-4 shadow-subtle">
          <div className="flex items-center space-x-2 text-xs font-bold text-brand-600 uppercase tracking-wider">
            <Key className="w-4 h-4" />
            <span>AI / LLM Reasoning Engine</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs font-semibold text-text-primary">Provider</label>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white"
              >
                <option value="smart_fallback">Smart Fallback (Zero-API-Key Offline Engine)</option>
                <option value="openai">OpenAI (GPT-4o, GPT-4 Turbo)</option>
                <option value="gemini">Google Gemini (Gemini 1.5 Pro)</option>
                <option value="anthropic">Anthropic (Claude 3.5 Sonnet)</option>
                <option value="ollama">Ollama (Local Llama 3 / DeepSeek)</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-text-primary">Model Identifier</label>
              <input
                type="text"
                value={model}
                onChange={(e) => setModel(e.target.value)}
                className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white"
              />
            </div>
          </div>

          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs">
              <label className="font-semibold text-text-primary">API Key</label>
              <span className="text-text-muted">Current: {settings?.masked_llm_key}</span>
            </div>
            <div className="relative">
              <input
                type={showApiKey ? "text" : "password"}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter new API key to update..."
                className="w-full px-3 py-2 pr-10 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white font-mono"
              />
              <button
                type="button"
                onClick={() => setShowApiKey(!showApiKey)}
                className="absolute right-3 top-2.5 text-text-muted hover:text-text-primary"
              >
                {showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>
        </div>

        {/* GitHub Integration */}
        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-4 shadow-subtle">
          <div className="flex items-center space-x-2 text-xs font-bold text-brand-600 uppercase tracking-wider">
            <Shield className="w-4 h-4" />
            <span>GitHub Integration</span>
          </div>

          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs">
              <label className="font-semibold text-text-primary">GitHub Personal Access Token (PAT)</label>
              <span className="text-text-muted">Status: {settings?.has_github_token ? 'Configured' : 'Sandbox Mode Active'}</span>
            </div>
            <input
              type="password"
              value={githubToken}
              onChange={(e) => setGithubToken(e.target.value)}
              placeholder="ghp_••••••••••••••••••••••••••••••••"
              className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white font-mono"
            />
          </div>
        </div>

        {/* Review Preferences */}
        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-4 shadow-subtle">
          <span className="text-xs font-bold text-brand-600 uppercase tracking-wider">Review Pipeline Thresholds</span>

          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs">
              <label className="font-semibold text-text-primary">Minimum Finding Confidence Filter</label>
              <span className="font-bold text-brand-600">{Math.round(minConfidence * 100)}%</span>
            </div>
            <input
              type="range"
              min="0.50"
              max="0.95"
              step="0.05"
              value={minConfidence}
              onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
              className="w-full accent-brand-500 cursor-pointer"
            />
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2.5 rounded-lg text-xs font-semibold bg-brand-500 hover:bg-brand-600 text-white flex items-center space-x-2 shadow-sm transition-all disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? 'Saving...' : 'Save Configuration'}</span>
          </button>
        </div>
      </form>
    </div>
  );
};
