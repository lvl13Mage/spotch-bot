import './styles/styles.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import AppMain from './components/AppMain';

declare global {
  interface Window {
    electronAPI: {
      startTwitchAuth: () => Promise<string>;
    }
  }
}

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <AppMain />
  </React.StrictMode>
);

async function handleTwitchAuth() {
  try {
      const token = await window.electronAPI.startTwitchAuth();
      console.log('Received Twitch token:', token);
      // Handle successful authentication
  } catch (error) {
      console.error('Twitch authentication failed:', error);
      // Handle authentication failure
  }
}

console.log('👋 This message is being logged by "renderer.tsx", included via webpack');