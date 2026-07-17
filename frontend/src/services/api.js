const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const fetchInsights = async () => {
  const response = await fetch(`${API_BASE_URL}/insights`);
  if (!response.ok) throw new Error('Failed to fetch insights');
  return response.json();
};

export const fetchDrafts = async () => {
  const response = await fetch(`${API_BASE_URL}/drafts`);
  if (!response.ok) throw new Error('Failed to fetch drafts');
  return response.json();
};

export const fetchCompetitors = async () => {
  const response = await fetch(`${API_BASE_URL}/competitors`);
  if (!response.ok) throw new Error('Failed to fetch competitors');
  return response.json();
};

export const fetchSentiment = async () => {
  const response = await fetch(`${API_BASE_URL}/sentiment`);
  if (!response.ok) throw new Error('Failed to fetch sentiment');
  return response.json();
};

export const fetchRetention = async () => {
  const response = await fetch(`${API_BASE_URL}/retention`);
  if (!response.ok) throw new Error('Failed to fetch retention');
  return response.json();
};

export const triggerPipeline = async () => {
  const response = await fetch(`${API_BASE_URL}/pipeline/start`, { method: 'POST' });
  if (!response.ok) throw new Error('Failed to start pipeline');
  return response.json();
};

export const startContinuous = async () => {
  const response = await fetch(`${API_BASE_URL}/pipeline/start_continuous`, { method: 'POST' });
  if (!response.ok) throw new Error('Failed to start continuous mode');
  return response.json();
};

export const stopContinuous = async () => {
  const response = await fetch(`${API_BASE_URL}/pipeline/stop_continuous`, { method: 'POST' });
  if (!response.ok) throw new Error('Failed to stop continuous mode');
  return response.json();
};

export const getPipelineStatus = async () => {
  const response = await fetch(`${API_BASE_URL}/pipeline/status`);
  if (!response.ok) throw new Error('Failed to fetch status');
  return response.json();
};
