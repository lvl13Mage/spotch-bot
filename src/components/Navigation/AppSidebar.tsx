"use client"

import * as React from "react"
import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  GalleryVerticalEnd,
  Map,
  PieChart,
  SquareTerminal,
} from "lucide-react"

import { 
  SiTwitch,
  SiSpotify
 } from '@icons-pack/react-simple-icons'


import { NavMain } from "@/components/Navigation/NavMain"
import { NavConnections } from "@/components/Navigation/NavConnections"
import { NavUser } from "@/components/Navigation/NavUser"
import { TeamSwitcher } from "@/components/Navigation/TeamSwitcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"

import { routes } from '@/routesConfig';

// This is sample data.
const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "Acme Inc",
      logo: GalleryVerticalEnd,
      plan: "Enterprise",
    },
    {
      name: "Acme Corp.",
      logo: AudioWaveform,
      plan: "Startup",
    },
    {
      name: "Evil Corp.",
      logo: Command,
      plan: "Free",
    },
  ],
  navMain: [
    {
      title: "ChatBot",
      url: "/chatbot",
      icon: SquareTerminal,
    },
    {
      title: "Cooldowns",
      url: "/cooldowns",
      icon: Bot,
    },
    {
      title: "Security",
      url: "#",
      icon: BookOpen,
      isActive: true,
      items: [
        {
          title: "Song Blocklist",
          url: "#",
        },
        {
          title: "User Blocklist",
          url: "#",
        },

        {
          title: "Word Filter",
          url: "#",
        },
      ],
    },
  ],
  connections: [
    {
      name: "Twitch",
      url: "#",
      icon: SiTwitch,
    },
    {
      name: "Spotify",
      url: "#",
      icon: SiSpotify,
    },
    {
      name: "Streamer.bot",
      url: "#",
      icon: Bot,
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain {...routes} />
        <NavConnections {...routes} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
