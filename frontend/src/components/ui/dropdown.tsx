import { cn } from "@/lib/utils";

export function Dropdown({ items, className }: { items: any[]; className?: string }) {
  return (
    <div
      className={cn(
        "bg-popover text-popover-foreground shadow-md rounded-md p-2",
        className
      )}
    >
      {items.map((item, index) => (
        <div
          key={index}
          className="p-2 hover:bg-muted hover:text-muted-foreground rounded-md"
        >
          {item}
        </div>
      ))}
    </div>
  );
}