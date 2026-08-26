"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppSidebar } from "@/components/app-sidebar";
import { UploadDialogProvider, useUploadDialog } from "@/contexts/upload-dialog-context";
import { UploadDialog } from "@/components/upload-dialog";

function DashboardShell({ children }: { children: React.ReactNode }) {
  const { open, setOpen } = useUploadDialog();

  return (
    <div className="flex min-h-screen bg-background">
      <AppSidebar />
      <main className="flex-1 px-6 py-8 md:px-10 md:py-10">{children}</main>
      <UploadDialog open={open} onOpenChange={setOpen} />
    </div>
  );
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.replace("/login");
      return;
    }
    setChecked(true);
  }, [router]);

  if (!checked) return null;

  return (
    <UploadDialogProvider>
      <DashboardShell>{children}</DashboardShell>
    </UploadDialogProvider>
  );
}
