import { apiClient } from './api';
import { SettingsData } from '../types';

export const settingsService = {
  async getSettings(): Promise<SettingsData> {
    const res = await apiClient.get<SettingsData>('/settings');
    return res.data;
  },

  async updateSettings(payload: Partial<SettingsData> & { llm_api_key?: string; github_token?: string }): Promise<SettingsData> {
    const res = await apiClient.post<SettingsData>('/settings', payload);
    return res.data;
  }
};
