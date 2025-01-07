import { ChartNoAxesColumnIcon, ChevronRight, type LucideIcon } from "lucide-react"
import { Link } from 'react-router-dom';

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar"
import { SimpleIcon } from "simple-icons"
import { IconType } from '@icons-pack/react-simple-icons';

import { RouteDefinition, RoutesConfig } from "@/routesConfig";

function VariableMenuItems({ childItemsLength = 0 }) {
  console.log("Child items:", childItemsLength)
  if ( childItemsLength > 0 ) {
    return <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
  }
}

function MenuItemLoader({ menuItem }: { menuItem: RouteDefinition }) {
  if (menuItem.children && menuItem.children.length > 0) {
    return (
      <Collapsible
        defaultOpen={menuItem.isActive}
        className="group/collapsible"
      >

        <SidebarMenuItem>
          <CollapsibleTrigger asChild>
            <SidebarMenuButton tooltip={menuItem.label}>
              {menuItem.icon && <menuItem.icon />}
              <Link to={menuItem.path}>
                <span>{menuItem.label}</span>
              </Link>
              <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
            </SidebarMenuButton>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <SidebarMenuSub>
              {menuItem.children?.map((subItem) => (
                <SidebarMenuSubItem key={subItem.path}>
                  <Link to={subItem.path}>
                    <SidebarMenuSubButton asChild>
                        <span>{subItem.label}</span>
                    </SidebarMenuSubButton>
                  </Link>
                </SidebarMenuSubItem>
              ))}
            </SidebarMenuSub>
          </CollapsibleContent>
        </SidebarMenuItem>
      </Collapsible>
    )
  } else {
    return (
      <SidebarMenuItem>
        <Link to={menuItem.path}>
          <SidebarMenuButton tooltip={menuItem.label}>
            {menuItem.icon && <menuItem.icon />}
              <span>{menuItem.label}</span>
          </SidebarMenuButton>
        </Link>
      </SidebarMenuItem>
    )
  }
}

export function NavMain({ botsettings, connectionsettings }: RoutesConfig) {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>Bot Settings</SidebarGroupLabel>
      <SidebarMenu>
        {botsettings.map((item) => (
          <MenuItemLoader key={item.path} menuItem={item} />
        ))}
      </SidebarMenu>
    </SidebarGroup>
  )
}
