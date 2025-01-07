import { app, BrowserWindow, ipcMain } from 'electron';
import express from 'express';
import { URL, URLSearchParams } from 'url';
import { TwitchAuthenticator } from '@/twitchapi/TwitchAuthenticator';

export class TwitchAuthService {
    private authenticator: TwitchAuthenticator;
    private server: express.Application | null = null;

    constructor() {
        this.authenticator = new TwitchAuthenticator();
        this.setupIpcListeners();
    }

    private setupIpcListeners() {
        ipcMain.handle('start-twitch-auth', async (event, { clientId, redirectPort }) => {
            return this.startAuthFlow(clientId, redirectPort);
        });

        ipcMain.handle('get-twitch-token', () => {
            return this.authenticator.getToken();
        });
    }


    private async startAuthFlow(clientId: string, redirectPort: number): Promise<string> {
        this.authenticator = new TwitchAuthenticator(clientId, redirectPort);
        await this.startRedirectServer();

        const authUrl = this.authenticator.getAuthUrl();
        const win = new BrowserWindow({ width: 800, height: 600 });
        win.loadURL(authUrl);

        return new Promise((resolve, reject) => {
            this.authenticator.onTokenReceived = (token) => {
                this.stopRedirectServer();
                win.close();
                resolve(token);
            };
        });
    }

    private async startRedirectServer() {
        return new Promise<void>((resolve) => {
            this.server = express();

            this.server.get('/auth/callback', (req, res) => {
                res.send('<html><body><script>window.location.href = "http://localhost:' + this.authenticator.redirectPort + '/auth/callback#" + window.location.hash.substr(1);</script></body></html>');
            });

            this.server.get('/auth/callback#', (req, res) => {
                const fullUrl = `${req.protocol}://${req.get('host')}${req.originalUrl}`;
                const parsedUrl = new URL(fullUrl);
                const hash = parsedUrl.hash.substr(1);
                const token = new URLSearchParams(hash).get('access_token');

                if (token) {
                    this.authenticator.setToken(token);
                    if (this.authenticator.onTokenReceived) {
                        this.authenticator.onTokenReceived(token);
                    }
                    res.send('<html><body><h1>Authentication successful!</h1><p>You can close this window now.</p></body></html>');
                } else {
                    res.status(400).send('<html><body><h1>Authentication failed</h1><p>No token received.</p></body></html>');
                }
            });

            this.server.listen(this.authenticator.redirectPort, () => {
                console.log(`Redirect server is running on http://localhost:${this.authenticator.redirectPort}`);
                resolve();
            });
        });
    }

    private stopRedirectServer() {
        if (this.server) {
            this.server.listen().close();
            this.server = null;
        }
    }
}