"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useAuthUser } from "@/hooks/use-auth-user";
import { useUploadDialog } from "@/contexts/upload-dialog-context";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  LayoutDashboard,
  Settings,
  CreditCard,
  UploadCloud,
  LogOut,
} from "lucide-react";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/dashboard/settings", label: "Settings", icon: Settings },
  { href: "/dashboard/plan", label: "Plan", icon: CreditCard },
];

export function AppSidebar() {
  const pathname = usePathname();
  const { user, initials, signOut } = useAuthUser();
  const { openDialog } = useUploadDialog();

  return (
    <aside className="flex h-full w-64 shrink-0 flex-col overflow-y-auto border-r border-border bg-background">
      <div className="px-6 py-6">
        <Link href="/dashboard" className="font-display text-xl tracking-tight">
          VAULT
        </Link>
      </div>

      {/* Profile */}
      <div className="flex items-center gap-3 px-6 pb-6">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-foreground text-sm font-semibold text-background">
          {initials}
        </div>
        <div className="min-w-0">
          <p className="truncate text-sm font-medium">{user?.name ?? "—"}</p>
          <p className="truncate text-xs text-muted-foreground">{user?.email ?? ""}</p>
        </div>
      </div>

      <Separator />

      {/* Nav */}
      <nav className="flex-1 space-y-1 px-4 py-6">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "bg-foreground text-background"
                  : "text-foreground/80 hover:bg-secondary"
              )}
            >
              <Icon className="h-4 w-4" strokeWidth={1.75} />
              {label}
            </Link>
          );
        })}

        <Button
          variant="outline"
          className="mt-2 w-full justify-start gap-3"
          onClick={openDialog}
        >
          <UploadCloud className="h-4 w-4" strokeWidth={1.75} />
          Upload document
        </Button>
      </nav>

      <Separator />

      <div className="shrink-0 px-4 py-4">
        <Button
          variant="ghost"
          className="w-full justify-start gap-3 text-muted-foreground hover:text-foreground"
          onClick={signOut}
        >
          <LogOut className="h-4 w-4" strokeWidth={1.75} />
          Sign out
        </Button>
      </div>
    </aside>
  );
}