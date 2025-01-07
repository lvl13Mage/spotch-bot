export interface RouteDefinition {
  path: string;
  label: string;
  component: React.ComponentType;
  icon?: React.ComponentType;
  children?: RouteDefinition[];
  isActive?: boolean;
}

export interface RoutesConfig {
  botsettings: RouteDefinition[];
  connectionsettings: RouteDefinition[];
}

  import {
    AudioWaveform,
    BookOpen,
    Bot,
    Command,
    GalleryVerticalEnd,
    SquareTerminal,
  } from "lucide-react"
  
  import { 
    SiTwitch,
    SiSpotify
   } from '@icons-pack/react-simple-icons'
  
  // Example pages (import your actual components)
  import Home from '@/components/Pages/Home';
  import ChatBot from '@/components/Pages/BotSettings/ChatBot';
  import Cooldowns from '@/components/Pages/BotSettings/Cooldowns';
  import Security from '@/components/Pages/BotSettings/Security';
  import SongBlocklist from '@/components/Pages/BotSettings/Security/SongBlocklist';
  import UserBlocklist from '@/components/Pages/BotSettings/Security/UserBlocklist';
  import WordFilter from '@/components/Pages/BotSettings/Security/WordFilter';
  import Spotify from '@/components/Pages/ConnectionSettings/Spotify';
  import StreamerBot from '@/components/Pages/ConnectionSettings/StreamerBot';
  import Twitch from '@/components/Pages/ConnectionSettings/Twitch';



  export const routes: RoutesConfig = {
    botsettings: [
      {
        path: '/',
        label: 'Home',
        component: Home,
      },
      {
        path: '/bot_settings/chatbot',
        label: 'Chat Bot',
        component: ChatBot,
        icon: SquareTerminal,
      },
      {
        path: '/bot_settings/cooldowns',
        label: 'Cooldowns',
        component: Cooldowns,
        icon: Bot,
      },
      {
        path: '/bot_settings/security',
        label: 'Security',
        component: Security,
        icon: BookOpen,
        isActive: true,
        children: [
          {
            path: '/bot_settings/security/song_blocklist',
            label: 'Song Blocklist',
            component: SongBlocklist,
          },
          {
            path: '/bot_settings/security/user_blocklist',
            label: 'User Blocklist',
            component: UserBlocklist,
          },
          {
            path: '/bot_settings/security/word_filter',
            label: 'Word Filter',
            component: WordFilter,
          },
        ]
      },
    ],
    connectionsettings: [
      {
        path: '/connection_settings/spotify',
        label: 'Spotify',
        component: Spotify,
        icon: SiTwitch,
      },
      {
        path: '/connection_settings/streamer_bot',
        label: 'Streamer.bot',
        component: StreamerBot,
        icon: SiSpotify,
      },
      {
        path: '/connection_settings/twitch',
        label: 'Twitch',
        component: Twitch,
        icon: Bot,
      }
    ]
  };