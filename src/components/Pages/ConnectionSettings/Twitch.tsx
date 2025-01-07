import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Eye, EyeOff } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Twitch: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showToken, setShowToken] = useState(false);
  const [token, setToken] = useState('');
  const [clientId, setClientId] = useState('');
  const [redirectPort, setRedirectPort] = useState(3000);

  const handleAuthenticate = async () => {
    try {
      const newToken = await window.electron.ipcRenderer.invoke('start-twitch-auth', { clientId, redirectPort });
      setToken(newToken);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Authentication failed:', error);
    }
  };

  return (
    <div>
      <h2>Twitch Authentication</h2>
      <div className="mb-4">
        <Label htmlFor="clientId">Client ID:</Label>
        <Input
          id="clientId"
          value={clientId}
          onChange={(e) => setClientId(e.target.value)}
          placeholder="Enter your Twitch Client ID"
        />
      </div>
      <div className="mb-4">
        <Label htmlFor="redirectPort">Redirect Port:</Label>
        <Input
          id="redirectPort"
          type="number"
          value={redirectPort}
          onChange={(e) => setRedirectPort(Number(e.target.value))}
          placeholder="Enter redirect port (default: 3000)"
        />
      </div>
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="outline" disabled={!clientId}>Authenticate with Twitch</Button>
        </DialogTrigger>
        <DialogContent 
          className="sm:max-w-[425px]"
          style={{ 
            position: 'fixed', 
            top: '50%', 
            left: '50%', 
            transform: 'translate(-50%, -50%)' 
          }}
        >
          <DialogHeader>
            <DialogTitle>Authenticate with Twitch</DialogTitle>
          </DialogHeader>
          <DialogDescription>
            This dialog allows you to authenticate with Twitch to access various features.
          </DialogDescription>
          <div>
            <p>Click the button below to start the Twitch authentication process:</p>
            <Button onClick={handleAuthenticate}>Start Authentication</Button>
          </div>
        </DialogContent>
      </Dialog>

      {isAuthenticated && (
        <div className="mt-4">
          <Label htmlFor="token">Twitch Token:</Label>
          <div className="flex items-center">
            <Input
              id="token"
              type={showToken ? 'text' : 'password'}
              value={token}
              readOnly
              className="mr-2"
            />
            <Button
              variant="outline"
              size="icon"
              onClick={() => setShowToken(!showToken)}
            >
              {showToken ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Twitch;