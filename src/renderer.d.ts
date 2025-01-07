interface Window {
    electron: {
      ipcRenderer: {
        send(channel: string, data: any): void;
        on(channel: string, func: (...args: any[]) => void): void;
        invoke(channel: string, ...args: any[]): Promise<any>;
      };
    };
  }