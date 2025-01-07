import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electron', {
  ipcRenderer: {
    send: (channel: string, data: any) => ipcRenderer.send(channel, data),
    on: (channel: string, func: (...args: any[]) => void) => 
      ipcRenderer.on(channel, (event, ...args) => func(...args)),
    invoke: (channel: string, ...args: any[]) => ipcRenderer.invoke(channel, ...args),
  },
});