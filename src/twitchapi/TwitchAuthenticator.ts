export class TwitchAuthenticator {
    private clientId: string;
    public redirectPort: number;
    private scopes: string[];
    private token: string | null = null;

    constructor(clientId: string = '', redirectPort: number = 3000) {
        this.clientId = clientId;
        this.redirectPort = redirectPort;
        this.scopes = [
            'chat:read',
            'chat:edit',
            'channel:manage:broadcast',
            'channel:read:redemptions',
            'channel:manage:redemptions',
            'channel:read:subscriptions',
            'channel:manage:polls',
            'channel:read:polls',
            'channel:manage:predictions',
            'channel:read:predictions',
            'moderation:read',
            'moderator:manage:banned_users',
            'moderator:manage:chat_messages',
            'moderator:read:chatters',
            'moderator:read:followers',
            'whispers:read',
            'whispers:edit'
        ];
    }

    public onTokenReceived: ((token: string) => void) | null = null;

    public getAuthUrl(): string {
        return `https://id.twitch.tv/oauth2/authorize?client_id=${this.clientId}&redirect_uri=${encodeURIComponent(this.redirectUri)}&response_type=token&scope=${this.scopes.join(' ')}`;
    }

    private get redirectUri() {
        return `http://localhost:${this.redirectPort}/auth/callback`;
    }

    public setToken(token: string) {
        this.token = token;
    }

    public getToken(): string | null {
        return this.token;
    }
}